#!/usr/bin/env python3
"""Bounded exposure-artifact probe (LEAD-only, safe-by-default).

Checks a small, high-signal catalog of information-disclosure paths (VCS
metadata, env/config, backups, API maps, diagnostics, source maps) against an
authorized host and classifies each response **without downloading bulk data**.

Design rules:
  * GET only, low volume, optional rate limit, hard cap on paths.
  * Redirect hops pass through `tools.safe_http.safe_urlopen` (SSRF + optional
    scope guard). Private/loopback/metadata destinations are blocked.
  * A 200 is never reported as a finding. Classification requires a content
    marker (e.g. `ref: refs/` for .git/HEAD, `DB_PASSWORD=` for .env).
  * Body content is inspected in memory (first N bytes) and never printed or
    written; only the matched marker name is emitted.
  * Output verdicts: LEAD | UNVERIFIED | SUSPECT_HTML | BLOCKED | EMPTY |
    REDIRECT | RATE_LIMIT | ERROR.

Usage:
  tools/exposure_probe.py -u https://target.com
  tools/exposure_probe.py -u https://target.com --max-paths 12 --rate 1.0
  tools/exposure_probe.py -u https://target.com --in-scope target.com --in-scope '*.target.com'
  tools/exposure_probe.py -u https://target.com --json --out exposure.jsonl
  tools/exposure_probe.py -u https://target.com --dry-run

Authorized targets only. Review every LEAD manually before reporting.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
from tools.safe_http import safe_urlopen  # noqa: E402

USER_AGENT = "agentic-bug-hunter/exposure_probe"
MAX_BODY_BYTES = 8192

# Ordered by typical impact. Deliberately small: this is not a brute-force list.
CATALOG: list[str] = [
    "/.git/HEAD",
    "/.git/config",
    "/.svn/wc.db",
    "/.env",
    "/.env.local",
    "/.env.production",
    "/.env.backup",
    "/wp-config.php",
    "/wp-config.php.bak",
    "/config.php",
    "/appsettings.json",
    "/web.config",
    "/WEB-INF/web.xml",
    "/.aws/credentials",
    "/backup.zip",
    "/backup.tar.gz",
    "/backup.sql",
    "/dump.sql",
    "/database.sql",
    "/swagger.json",
    "/openapi.json",
    "/v3/api-docs",
    "/api-docs",
    "/swagger-ui.html",
    "/graphql",
    "/actuator",
    "/actuator/env",
    "/actuator/health",
    "/phpinfo.php",
    "/server-status",
    "/trace.axd",
    "/elmah.axd",
    "/storage/logs/laravel.log",
    "/error.log",
    "/_profiler",
    "/telescope/requests",
    "/metrics",
    "/debug/pprof/",
    "/package-lock.json",
    "/composer.lock",
    "/.DS_Store",
    "/humans.txt",
    "/.well-known/security.txt",
]

# Marker -> (class, label). Markers are matched case-sensitively unless noted.
_MARKERS: list[tuple[str, str, str, bool]] = [
    ("ref: refs/", "VCS_METADATA", "git_head", False),
    ('[core]', "VCS_METADATA", "git_config", False),
    ("SQLite format 3", "VCS_METADATA", "svn_wc_db", False),
    ('"sourcesContent"', "SOURCE_MAP", "source_map", False),
    ('"mappings"', "SOURCE_MAP", "source_map", False),
    ('"openapi"', "API_SPEC", "openapi", False),
    ('"swagger"', "API_SPEC", "swagger", False),
    ('"paths"', "API_SPEC", "api_paths", False),
    ('"propertySources"', "DIAGNOSTIC_SURFACE", "actuator_env", False),
    ("activeProfiles", "DIAGNOSTIC_SURFACE", "actuator_env", False),
    ("Apache Server Status", "DIAGNOSTIC_SURFACE", "server_status", False),
    ("PHP Version", "DIAGNOSTIC_SURFACE", "phpinfo", False),
    ("phpinfo()", "DIAGNOSTIC_SURFACE", "phpinfo", False),
    ("Error Log for", "DIAGNOSTIC_SURFACE", "elmah", False),
    ("INSERT INTO", "BACKUP_DUMP", "sql_dump", False),
    ("CREATE TABLE", "BACKUP_DUMP", "sql_dump", False),
    ("Index of /", "DIR_LISTING", "dir_listing", False),
    ("local.ERROR", "LOG_EXPOSURE", "laravel_log", False),
    ("production.ERROR", "LOG_EXPOSURE", "laravel_log", False),
    ("AWS_SECRET_ACCESS_KEY", "ENV_CONFIG_EXPOSURE", "env", False),
    ("DB_PASSWORD", "ENV_CONFIG_EXPOSURE", "env", False),
    ("DATABASE_URL", "ENV_CONFIG_EXPOSURE", "env", False),
    ("SECRET_KEY", "ENV_CONFIG_EXPOSURE", "env", False),
    ("APP_KEY", "ENV_CONFIG_EXPOSURE", "env", False),
    ("BEGIN RSA PRIVATE KEY", "SECRET_LIKE_TOKEN", "private_key", False),
    ("BEGIN OPENSSH PRIVATE KEY", "SECRET_LIKE_TOKEN", "private_key", False),
]

_PLACEHOLDER_RE = re.compile(
    r"(?i)(changeme|change_me|your[-_]?key|example\.com|<[^>]+>|xxx+|placeholder|dummy)"
)


@dataclass
class ProbeResult:
    url: str
    path: str
    status: int
    content_type: str
    verdict: str
    disclosure_class: str = ""
    marker: str = ""
    note: str = ""
    bytes_inspected: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def _marker_allowed(marker_label: str, path: str) -> bool:
    """Path-context guard for generic markers (reduces false LEADs)."""
    p = (path or "").lower()
    if marker_label in {"api_paths"}:
        return any(k in p for k in ("swagger", "openapi", "api-docs", "redoc", "graphql"))
    if marker_label == "source_map":
        return p.endswith(".map") or "source" in p
    if marker_label in {"actuator_env", "phpinfo", "elmah", "server_status"}:
        key = {"actuator_env": "actuator", "phpinfo": "phpinfo",
               "elmah": "elmah", "server_status": "server-status"}[marker_label]
        return key in p or (marker_label == "phpinfo" and p.rstrip("/").endswith(("/info.php", "/test.php", "/i.php")))
    if marker_label == "env":
        return any(k in p for k in ("env", "config", "settings", "credentials", "application", ".npmrc", ".aws"))
    if marker_label == "sql_dump":
        return any(k in p for k in ("sql", "dump", "backup", "database", "db."))
    if marker_label == "laravel_log":
        return "log" in p
    return True


def _looks_html(content_type: str, body: str) -> bool:
    ct = (content_type or "").lower()
    if "html" in ct:
        return True
    head = body[:400].lstrip().lower()
    return head.startswith("<!doctype html") or head.startswith("<html") or "<head" in head


def classify_response(
    path: str,
    status: int,
    content_type: str,
    body: str,
    location: str = "",
) -> tuple[str, str, str, str]:
    """Pure classifier -> (verdict, disclosure_class, marker, note).

    A 200 alone is UNVERIFIED/SUSPECT_HTML. LEAD requires a real content marker.
    """
    if status == 0:
        return "ERROR", "", "", "request failed"
    if status == 429:
        return "RATE_LIMIT", "", "", "back off"
    if status in (401, 403):
        return "BLOCKED", "", "", "auth required / forbidden"
    if status in (404, 410):
        return "EMPTY", "", "", "not present"
    if 300 <= status < 400:
        return "REDIRECT", "", "", f"location={location[:120]}" if location else "redirect"
    if status >= 500:
        return "ERROR", "", "", f"server error {status}"
    if not (200 <= status < 300):
        return "UNVERIFIED", "", "", f"status {status}"

    if _looks_html(content_type, body):
        return "SUSPECT_HTML", "", "", "HTML shell, not the artifact"

    for marker, klass, label, _ in _MARKERS:
        if marker in body and _marker_allowed(label, path):
            if _PLACEHOLDER_RE.search(body[:2000]) and klass in {"ENV_CONFIG_EXPOSURE", "SECRET_LIKE_TOKEN"}:
                return "UNVERIFIED", klass, label, "placeholder-like value"
            return "LEAD", klass, label, f"marker={label}"

    return "UNVERIFIED", "", "", "2xx without a known marker"


def _fetch(url: str, timeout: float, scope_checker=None) -> tuple[int, str, str, str]:
    req = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": USER_AGENT, "X-Bug-Bounty": "agentic-bug-hunter"},
    )
    try:
        resp = safe_urlopen(
            req, timeout=timeout, max_redirects=3, scope_checker=scope_checker
        )
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError) as exc:
        return 0, "", "", str(exc)[:160]
    status = getattr(resp, "status", 0) or getattr(resp, "code", 0) or 0
    headers = getattr(resp, "headers", None)
    content_type = headers.get("Content-Type", "") if headers else ""
    location = headers.get("Location", "") if headers else ""
    body = ""
    try:
        raw = resp.read(MAX_BODY_BYTES) or b""
        body = raw.decode("utf-8", errors="ignore")
    except Exception:
        body = ""
    finally:
        try:
            resp.close()
        except Exception:
            pass
    return status, content_type, body, location


def build_targets(base_url: str, paths: list[str]) -> list[tuple[str, str]]:
    base = (base_url or "").strip()
    if not base:
        raise ValueError("invalid base URL: empty")
    base = base if "://" in base else f"https://{base}"
    parsed = urllib.parse.urlparse(base)
    if not parsed.scheme or not parsed.netloc or not parsed.netloc.strip():
        raise ValueError(f"invalid base URL: {base_url!r}")
    base = f"{parsed.scheme}://{parsed.netloc}"
    return [(p, urllib.parse.urljoin(base + "/", p.lstrip("/"))) for p in paths]


def _load_scope(patterns: list[str], excluded: list[str]):
    if not patterns:
        return None
    from tools.scope_checker import ScopeChecker

    return ScopeChecker(patterns, excluded)


def run_probe(
    base_url: str,
    paths: list[str],
    timeout: float = 8.0,
    rate: float = 0.5,
    scope_checker=None,
    dry_run: bool = False,
) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    for path, url in build_targets(base_url, paths):
        if scope_checker is not None and not scope_checker.is_in_scope(url):
            results.append(ProbeResult(url=url, path=path, status=0, content_type="",
                                       verdict="SKIPPED", note="out of scope"))
            continue
        if dry_run:
            results.append(ProbeResult(url=url, path=path, status=0, content_type="",
                                       verdict="PLANNED", note="dry-run"))
            continue
        status, ctype, body, location = _fetch(url, timeout, scope_checker)
        verdict, klass, marker, note = classify_response(path, status, ctype, body, location)
        results.append(ProbeResult(
            url=url, path=path, status=status, content_type=ctype[:80],
            verdict=verdict, disclosure_class=klass, marker=marker, note=note,
            bytes_inspected=len(body),
        ))
        if rate:
            time.sleep(rate)
    return results


def _print_table(results: list[ProbeResult]) -> None:
    width = max((len(r.path) for r in results), default=8)
    print(f"{'PATH'.ljust(width)}  {'STATUS':>6}  {'VERDICT':<14}  CLASS / NOTE")
    for r in results:
        detail = r.disclosure_class or ""
        if r.note:
            detail = f"{detail} ({r.note})" if detail else r.note
        print(f"{r.path.ljust(width)}  {r.status:>6}  {r.verdict:<14}  {detail}")
    leads = sum(1 for r in results if r.verdict == "LEAD")
    print(f"\n{leads} LEAD(s) / {len(results)} path(s). "
          "A LEAD is not a finding until validated on an in-scope asset.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bounded exposure-artifact probe (LEAD-only).")
    parser.add_argument("-u", "--url", required=True, help="Base URL or host")
    parser.add_argument("-l", "--paths", help="File with paths (one per line); default catalog")
    parser.add_argument("--max-paths", type=int, default=len(CATALOG), help="Hard cap on paths probed")
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--rate", type=float, default=0.5, help="Seconds between requests (0 disables)")
    parser.add_argument("--in-scope", action="append", default=[], help="Allowed domain pattern (repeatable)")
    parser.add_argument("--exclude", action="append", default=[], help="Excluded domain pattern (repeatable)")
    parser.add_argument("--json", action="store_true", help="JSONL output")
    parser.add_argument("--out", help="Write results to file")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan; no network requests")
    args = parser.parse_args(argv)

    if args.paths:
        try:
            paths = [ln.strip() for ln in Path(args.paths).read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        except OSError as exc:
            parser.error(f"cannot read paths file: {exc}")
    else:
        paths = list(CATALOG)

    if not paths:
        parser.error("no paths to probe")
    if args.max_paths < 1:
        parser.error("--max-paths must be >= 1")
    paths = paths[: args.max_paths]

    try:
        scope_checker = _load_scope(args.in_scope, args.exclude)
    except Exception as exc:  # ScopeError and friends
        parser.error(f"invalid scope config: {exc}")

    try:
        results = run_probe(
            args.url, paths, timeout=args.timeout, rate=args.rate,
            scope_checker=scope_checker, dry_run=args.dry_run,
        )
    except ValueError as exc:
        parser.error(str(exc))

    lines = [json.dumps(asdict(r), ensure_ascii=False) for r in results]
    payload = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(payload + "\n", encoding="utf-8")
    if args.json:
        print(payload)
    else:
        _print_table(results)
        if args.out:
            print(f"\nJSONL written to {args.out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())