#!/usr/bin/env python3
"""Deep API tester over the app-model — test endpoints, not just route leads.

The lead board only routes a handful of signals; a real target has thousands of
endpoints (temu: ~6,000) and "no findings" too often means "never tested". This
walks the deduplicated app-model and classifies each endpoint, with a **per-host
baseline** so bot-management shells / SPA catch-alls are not mistaken for public
endpoints.

Per endpoint it records (read-only by default: GET/HEAD/OPTIONS only):
  PUBLIC          anon 2xx (candidate missing-authz — verify it's not intended)
  AUTH_REQUIRED   anon 401/403
  AUTHZ_DELTA     anon != identity-A (with --identity) -> inspect
  REDIRECT        3xx
  METHOD_*        from OPTIONS/Allow
  SERVER_ERROR    5xx
  BLOCKED_SHELL   response ≈ the host's nonexistent-path baseline (bot/SPA shell)
  UNKNOWN/ERROR

Writes:
  <out>/api_probe.jsonl   one classified row per tested endpoint
  <out>/coverage.json     {tested,total,pct,by_verdict} -> consumed by hunt_outcome

Usage:
  python3 -m tools.api_probe --target temu.com --recon-dir bughunter/recon/temu.com --max-endpoints 200
  # with an identity (test authz): --identity /tmp/session.json
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools import app_model  # noqa: E402
from tools.verifiers.base import fetch  # noqa: E402

SIGNAL = {"PUBLIC", "AUTHZ_DELTA", "METHOD_PUT", "METHOD_DELETE", "SERVER_ERROR"}


def endpoint_url(base: str, key: str) -> str:
    path = key.split(" ", 1)[1] if " " in key else key
    if path.startswith("http"):
        return path
    return base.rstrip("/") + "/" + path.lstrip("/")


def classify(anon_status, anon_len, base_status, base_len, auth_status=None,
             allow=None) -> str:
    """Pure classifier (unit-tested)."""
    if anon_status is None:
        return "ERROR"
    # bot-management / SPA catch-all: same as the nonexistent-path baseline.
    # Only for a *substantial* baseline body (>=200B) so a tiny catch-all cannot
    # swallow every small 200 response into BLOCKED_SHELL.
    if base_status is not None and anon_status == base_status and (base_len or 0) >= 200:
        band = max(24, int(0.05 * max(base_len, 1)))
        if abs((anon_len or 0) - (base_len or 0)) <= band:
            return "BLOCKED_SHELL"
    if allow and "PUT" in allow:
        return "METHOD_PUT"
    if allow and "DELETE" in allow:
        return "METHOD_DELETE"
    if 200 <= anon_status < 300:
        if auth_status is not None and auth_status in (401, 403):
            return "AUTHZ_DELTA"          # anon allowed, identity denied -> odd
        return "PUBLIC"
    if anon_status in (401, 403):
        if auth_status is not None and 200 <= auth_status < 300:
            return "AUTH_REQUIRED"        # normal: anon denied, identity allowed
        return "AUTH_REQUIRED"
    if anon_status in (301, 302, 303, 307, 308):
        return "REDIRECT"
    if anon_status == 405:
        return "METHOD_NOT_ALLOWED"
    if 500 <= anon_status < 600:
        return "SERVER_ERROR"
    return "OTHER"


def _host(url: str) -> str:
    from urllib.parse import urlsplit
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}" if p.scheme and p.netloc else ""


def _allow_from(opts) -> str:
    hdrs = opts.response_headers or {}
    for k, v in hdrs.items():
        if k.lower() == "allow":
            return str(v).upper()
    return ""


def build_coverage(target: str, tested: int, total: int, verdicts: dict) -> dict:
    return {
        "schema": "api-coverage/1",
        "target": target,
        "tested": tested,
        "total": total,
        "pct": round(tested / total, 4) if total else 0.0,
        "by_verdict": dict(sorted(verdicts.items())),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def run(target: str, recon_dir: str, *, max_endpoints: int = 200,
        identity_headers: dict | None = None, scope_checker=None,
        out_dir: str | None = None, delay: float = 0.05) -> dict:
    model = app_model.build(target, recon_dir=recon_dir)
    eps = model["endpoints"]
    total = len(eps)
    out_dir = out_dir or os.path.join(_REPO, "findings", target, "api_probe")
    os.makedirs(out_dir, exist_ok=True)

    # per-host baseline (one nonexistent-path probe per host)
    bases: dict[str, tuple] = {}
    for e in eps[:max_endpoints]:
        url = endpoint_url(e.get("base_url") or f"https://{target}", e["key"])
        host = _host(url)
        if host and host not in bases:
            ex, body = fetch(host + f"/__zzq_{secrets.token_hex(3)}__",
                             scope_checker=scope_checker, timeout=8, note="api baseline")
            bases[host] = (ex.status, len(body))

    rows, verdicts, tested = [], {}, 0
    for e in eps[:max_endpoints]:
        base = e.get("base_url") or f"https://{target}"
        url = endpoint_url(base, e["key"])
        bs, bl = bases.get(_host(url), (None, 0))
        ex, body = fetch(url, scope_checker=scope_checker, timeout=8, note="api probe")
        opts, _ = fetch(url, method="OPTIONS", scope_checker=scope_checker, timeout=8,
                        note="api options")
        auth_status = None
        if identity_headers:
            exa, _ = fetch(url, headers=identity_headers, scope_checker=scope_checker,
                           timeout=8, note="api identity")
            auth_status = exa.status
        verdict = classify(ex.status, len(body), bs, bl, auth_status, _allow_from(opts))
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        rows.append({"key": e["key"], "url": url, "anon": ex.status,
                     "base": bs, "auth": auth_status, "verdict": verdict})
        tested += 1
        if delay:
            time.sleep(delay)

    with open(os.path.join(out_dir, "api_probe.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    cov = build_coverage(target, tested, total, verdicts)
    with open(os.path.join(out_dir, "coverage.json"), "w") as fh:
        json.dump(cov, fh, indent=2)
    return {"coverage": cov, "rows": rows}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Deep API tester over the app-model")
    p.add_argument("--target", required=True)
    p.add_argument("--recon-dir", required=True)
    p.add_argument("--max-endpoints", type=int, default=200)
    p.add_argument("--identity", help="auth file ({\"headers\":[...]} or {\"cookie\":...})")
    p.add_argument("--scope-domain", action="append", default=[])
    p.add_argument("--out-dir")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    identity = None
    if args.identity:
        from tools.auth_session import AuthSession
        identity = AuthSession.from_file(args.identity).headers_dict()

    scope_checker = None
    if args.scope_domain:
        from tools.scope_checker import ScopeChecker
        scope_checker = ScopeChecker(args.scope_domain)

    res = run(args.target, args.recon_dir, max_endpoints=args.max_endpoints,
              identity_headers=identity, scope_checker=scope_checker, out_dir=args.out_dir)
    cov = res["coverage"]
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"API probe {args.target}: tested {cov['tested']}/{cov['total']} "
              f"({cov['pct']*100:.1f}%)  verdicts={cov['by_verdict']}")
        for r in res["rows"]:
            if r["verdict"] in SIGNAL:
                print(f"  [{r['verdict']}] {r['key']} (anon {r['anon']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())