#!/usr/bin/env python3
"""GitHub OSINT delta monitor for authorized bug-bounty programs.

Watches target GitHub organizations for changes that matter during recon:
new repositories, new commits (especially auth/CI/crypto/dependency changes),
new releases, workflow changes, and exposed secret/dependency alerts when the
token has access.

Design rules:
  - delta-first: only report what changed since the last run
  - read-only: no writes, no cloning, no execution of target code
  - scope-aware: pass only organizations/repos you are authorized to review
  - token-safe: the token is read from GITHUB_TOKEN and never printed

Usage:
  python3 bughunter/tools/github_osint_monitor.py --orgs acme,acme-labs
  python3 bughunter/tools/github_osint_monitor.py --orgs acme --json
  python3 bughunter/tools/github_osint_monitor.py --orgs acme --out output/osint

State defaults to memory/osint-state.json. Runs compare against the
stored state and only report changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

API = "https://api.github.com"
UA = "agentic-bug-hunter/github-osint-monitor"
SECURITY_WORDS = re.compile(
    r"\b(auth|oauth|oidc|jwt|token|secret|credential|password|passwd|key|"
    r"sign|signature|verify|crypto|permission|admin|privilege|security|"
    r"cve|vuln|fix|patch|bypass|redirect|ssrf|xss|rce|workflow|actions|"
    r"deploy|release|dependency|dependabot)\b",
    re.I,
)


class RateLimited(RuntimeError):
    def __init__(self, reset_epoch: int):
        self.reset_epoch = reset_epoch
        super().__init__(f"GitHub rate limit; reset at {reset_epoch}")


@dataclass
class RepoObservation:
    full_name: str
    html_url: str
    private: bool
    pushed_at: str
    default_branch: str
    description: str = ""
    latest_commit: str = ""
    latest_commit_at: str = ""
    latest_commit_message: str = ""
    release_tag: str = ""
    release_at: str = ""
    workflow_hash: str = ""
    secret_alerts: int = 0
    dependabot_alerts: int = 0


@dataclass
class Signal:
    kind: str
    repo: str
    detail: str
    url: str
    severity: str = "info"


def _headers(token: str | None) -> dict[str, str]:
    h = {"Accept": "application/vnd.github+json", "User-Agent": UA,
         "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _request(url: str, token: str | None, *, retries: int = 2) -> Any:
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers=_headers(token))
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429):
                reset = int(exc.headers.get("X-RateLimit-Reset", "0") or 0)
                if reset > int(time.time()):
                    raise RateLimited(reset) from exc
            if exc.code in (404, 451):
                return None
            if exc.code >= 500 and attempt < retries:
                time.sleep(1 + attempt)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries:
                time.sleep(1 + attempt)
                continue
            raise
    return None


def _get(url: str, token: str | None, params: dict[str, Any] | None = None) -> Any:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    return _request(url, token)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _workflow_hash(workflows: Any) -> str:
    if not isinstance(workflows, dict):
        return ""
    items = []
    for wf in workflows.get("workflows", []) or []:
        items.append((wf.get("path", ""), wf.get("state", ""), wf.get("updated_at", "")))
    return hashlib.sha256(json.dumps(sorted(items), separators=(",", ":")).encode()).hexdigest()[:16]


def is_security_commit(message: str) -> bool:
    text = (message or "").strip()
    if re.match(r"^(docs?|chore|style|tests?)\b", text, re.I):
        return bool(re.search(
            r"\b(auth|oauth|jwt|token|secret|credential|password|sign|signature|"
            r"verify|crypto|permission|admin|security|cve|vuln|bypass|ssrf|xss|rce|"
            r"workflow|actions|deploy|dependency)\b",
            text, re.I))
    return bool(SECURITY_WORDS.search(text))


def collect_repo(full_name: str, token: str | None, *, alert_limit: int = 20,
                 include_alerts: bool = True) -> RepoObservation:
    repo = _get(f"{API}/repos/{full_name}", token)
    if not isinstance(repo, dict):
        raise RuntimeError(f"repository not found or inaccessible: {full_name}")
    obs = RepoObservation(
        full_name=repo.get("full_name", full_name),
        html_url=repo.get("html_url", ""),
        private=bool(repo.get("private")),
        pushed_at=repo.get("pushed_at", "") or "",
        default_branch=repo.get("default_branch", "") or "",
        description=repo.get("description") or "",
    )

    commits = _get(f"{API}/repos/{full_name}/commits", token, {"per_page": 1})
    if isinstance(commits, list) and commits:
        c = commits[0]
        obs.latest_commit = c.get("sha", "")[:12]
        obs.latest_commit_at = (c.get("commit", {}).get("author", {}) or {}).get("date", "") or ""
        obs.latest_commit_message = (c.get("commit", {}).get("message", "") or "").splitlines()[0][:200]

    releases = _get(f"{API}/repos/{full_name}/releases", token, {"per_page": 1})
    if isinstance(releases, list) and releases:
        obs.release_tag = releases[0].get("tag_name", "") or ""
        obs.release_at = releases[0].get("published_at", "") or ""

    workflows = _get(f"{API}/repos/{full_name}/actions/workflows", token, {"per_page": 100})
    obs.workflow_hash = _workflow_hash(workflows)

    if include_alerts:
        try:
            alerts = _get(f"{API}/repos/{full_name}/secret-scanning/alerts", token,
                          {"state": "open", "per_page": alert_limit})
            if isinstance(alerts, list):
                obs.secret_alerts = len(alerts)
        except Exception:
            pass
        try:
            alerts = _get(f"{API}/repos/{full_name}/dependabot/alerts", token,
                          {"state": "open", "per_page": alert_limit})
            if isinstance(alerts, list):
                obs.dependabot_alerts = len(alerts)
        except Exception:
            pass
    return obs


def diff_repo(obs: RepoObservation, previous: dict[str, Any] | None) -> list[Signal]:
    prev = previous or {}
    signals: list[Signal] = []
    if not prev:
        signals.append(Signal("new_repo", obs.full_name, obs.description or "new repository", obs.html_url, "medium"))
    if obs.latest_commit and obs.latest_commit != prev.get("latest_commit"):
        sev = "high" if is_security_commit(obs.latest_commit_message) else "info"
        signals.append(Signal("new_commit", obs.full_name,
                              f"{obs.latest_commit} {obs.latest_commit_message}".strip(),
                              f"{obs.html_url}/commit/{obs.latest_commit}", sev))
    if obs.release_tag and obs.release_tag != prev.get("release_tag"):
        signals.append(Signal("new_release", obs.full_name, obs.release_tag, f"{obs.html_url}/releases", "medium"))
    if obs.workflow_hash and obs.workflow_hash != prev.get("workflow_hash"):
        signals.append(Signal("workflow_change", obs.full_name, "GitHub Actions workflow changed",
                              f"{obs.html_url}/actions", "medium"))
    if obs.secret_alerts > int(prev.get("secret_alerts", 0)):
        signals.append(Signal("secret_alert", obs.full_name,
                              f"{obs.secret_alerts} open secret-scanning alert(s)",
                              f"{obs.html_url}/security/secret-scanning", "high"))
    if obs.dependabot_alerts > int(prev.get("dependabot_alerts", 0)):
        signals.append(Signal("dependabot_alert", obs.full_name,
                              f"{obs.dependabot_alerts} open dependency alert(s)",
                              f"{obs.html_url}/security/dependabot", "medium"))
    return signals


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "orgs": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "orgs" in data:
            return data
    except Exception:
        pass
    return {"version": 1, "orgs": {}}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def render_markdown(signals: list[Signal], orgs: list[str], generated: str) -> str:
    lines = [
        "# GitHub OSINT delta",
        "",
        f"Generated: {generated}",
        f"Organizations: {', '.join(orgs)}",
        f"Signals: {len(signals)}",
        "",
        "| Severity | Signal | Repo | Detail |",
        "|---|---|---|---|",
    ]
    for s in signals:
        detail = s.detail.replace("|", "\\|")
        lines.append(f"| {s.severity} | {s.kind} | [{s.repo}]({s.url}) | {detail} |")
    if not signals:
        lines.append("| — | — | — | no changes |")
    lines.append("")
    lines.append("> Delta-only. A signal is a LEAD; verify scope, exploitability and impact before reporting.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Delta-first GitHub OSINT monitor for authorized targets.")
    parser.add_argument("--orgs", default="", help="Comma-separated GitHub orgs (e.g. acme,acme-labs)")
    parser.add_argument("--state", default="memory/osint-state.json", help="State JSON path")
    parser.add_argument("--out", default="output/osint", help="Output directory")
    parser.add_argument("--max-repos", type=int, default=100, help="Max repos per org")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    parser.add_argument("--no-alerts", action="store_true", help="Skip secret/dependabot alerts")
    parser.add_argument("--dry-run", action="store_true", help="Do not write state/output")
    args = parser.parse_args(argv)

    orgs = [o.strip() for o in args.orgs.split(",") if o.strip()]
    if not orgs:
        parser.error("--orgs is required (authorized organizations only)")

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    state_path = Path(args.state)
    state = load_state(state_path)
    now = datetime.now(timezone.utc)
    generated = _iso(now)
    all_signals: list[Signal] = []
    current: dict[str, Any] = {"version": 1, "updated": generated, "orgs": {}}

    for org in orgs:
        prev_org = state.get("orgs", {}).get(org, {})
        prev_repos = prev_org.get("repos", {})
        print(f"[*] {org}: scanning...", file=sys.stderr)
        repos = _get(f"{API}/orgs/{org}/repos", token,
                     {"sort": "pushed", "direction": "desc", "per_page": min(100, args.max_repos)})
        if not isinstance(repos, list):
            print(f"[!] {org}: organization not found or inaccessible", file=sys.stderr)
            current["orgs"][org] = prev_org
            continue
        org_repos: dict[str, Any] = {}
        for repo in repos[: args.max_repos]:
            full_name = repo.get("full_name")
            if not full_name:
                continue
            try:
                obs = collect_repo(full_name, token, include_alerts=not args.no_alerts)
            except RateLimited as exc:
                reset = datetime.fromtimestamp(exc.reset_epoch, tz=timezone.utc)
                print(f"[!] rate limited; retry after {_iso(reset)}", file=sys.stderr)
                break
            except Exception as exc:
                print(f"[!] {full_name}: {type(exc).__name__}: {exc}", file=sys.stderr)
                continue
            signals = diff_repo(obs, prev_repos.get(full_name))
            all_signals.extend(signals)
            org_repos[full_name] = asdict(obs)
            print(f"    {full_name}: {len(signals)} signal(s)", file=sys.stderr)
        current["orgs"][org] = {"repos": org_repos}

    all_signals.sort(key=lambda s: ({"high": 0, "medium": 1, "info": 2}.get(s.severity, 3), s.kind, s.repo))
    out = Path(args.out)
    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)
        (out / "osint-delta.md").write_text(render_markdown(all_signals, orgs, generated), encoding="utf-8")
        (out / "osint-delta.json").write_text(json.dumps([asdict(s) for s in all_signals], indent=2) + "\n",
                                              encoding="utf-8")
        save_state(state_path, current)

    if args.json:
        print(json.dumps([asdict(s) for s in all_signals], indent=2))
    else:
        print(render_markdown(all_signals, orgs, generated))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
