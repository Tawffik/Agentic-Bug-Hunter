#!/usr/bin/env python3
"""Hidden-parameter discovery — built-in fallback when arjun/x8 are absent.

Recon finds *paths*, but most impactful bugs (SSRF, open-redirect, SQLi, XSS,
IDOR) live on a **parameter** of that path. The toolkit's primary param tools
(`param_discovery.sh` -> arjun/x8) are optional installs; when they are missing
the pipeline silently discovers no parameters, so every param-class lead is
never even routed. This is the deterministic, dependency-free fallback.

Method (GET only, single-hop, scope-guarded, bounded):
  baseline  = response to the URL unchanged
  probe     = response to the URL with `?<param>=<random-canary>`
  candidate = status changed, OR body length moved beyond a noise band, OR the
              unique canary is reflected. A unique canary means a reflection-
              based param (XSS/open-redirect/SSRF input) is provable, not guessed.

It emits *leads*, never findings — one candidate URL per discovered parameter.

Usage:
  python3 -m tools.param_probe --url http://host/path [--url ...]
  python3 -m tools.param_probe --list endpoints.txt --out urls/with_params.txt
      [--scope-domain host --max-urls 50 --delay 0.2 --json]

Library:
  from tools.param_probe import discover
  urls = discover(endpoints, scope_checker=sc)   # -> ["http://host/p?q=canary", ...]
"""
from __future__ import annotations

import argparse
import os
import secrets
import sys
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools.verifiers.base import fetch  # noqa: E402

# Common parameter names, ordered by exploit value. Kept intentionally small so
# the probe is a bounded, low-noise sweep rather than a brute force.
DEFAULT_PARAMS = [
    "url", "uri", "redirect", "redirect_uri", "next", "return", "returnUrl",
    "continue", "dest", "destination", "target", "host", "domain", "callback",
    "file", "path", "page", "template", "include", "view", "folder", "doc",
    "id", "uid", "user", "user_id", "account", "order", "order_id", "invoice",
    "q", "s", "search", "query", "keyword", "name", "cmd", "exec", "debug",
    "admin", "config", "key", "token", "lang", "locale", "format", "type",
    "action", "ref", "source", "data", "json", "email",
]

_MIN_BODY_DELTA = 12

# Error-token signal: a syntax breaker that surfaces an error string the benign
# response lacks is a high-signal param (error-based SQLi/NoSQLi/template). Kept
# narrow so ordinary dynamic pages don't trip it.
_ERROR_TOKENS = (
    b"sql syntax", b"syntax error", b"sqlstate", b"you have an error in your sql",
    b"unclosed quotation", b"pg_query", b"mysql_", b"sqlite", b"odbc ",
    b"traceback (most recent", b"stack trace", b"org.springframework",
    b"system.data.sql", b"unexpected end of input", b"templateerror",
)


def _with_param(url: str, param: str, value: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query, keep_blank_values=True)
    query[param] = [value]
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def response_changed(base_status, base_body: bytes, probe_status, probe_body: bytes,
                     canary: str) -> tuple[bool, str]:
    """Pure decision function (unit-tested). Returns (changed, why)."""
    if base_status is None or probe_status is None:
        return False, "no response"
    if probe_status != base_status:
        return True, f"status {base_status}->{probe_status}"
    if canary.encode() in probe_body and canary.encode() not in base_body:
        return True, "canary reflected"
    low_p = probe_body.lower()
    low_b = base_body.lower()
    for tok in _ERROR_TOKENS:
        if tok in low_p and tok not in low_b:
            return True, f"error signature: {tok.decode(errors='replace')}"
    delta = abs(len(probe_body) - len(base_body))
    band = max(_MIN_BODY_DELTA, int(0.05 * max(len(base_body), 1)))
    if delta > band:
        return True, f"body length delta {delta}"
    return False, ""


def _location(ex) -> str:
    hdr = ex.response_headers or {}
    for k, v in hdr.items():
        if k.lower() == "location":
            return str(v)
    return ""


def probe(url: str, param: str, *, scope_checker=None, canary: str | None = None,
          timeout: float = 10.0) -> tuple[bool, str, str]:
    """Probe one (url, param). Returns (changed, why, probe_url).

    Three signals, in order: (1) a reflection/length/status delta on a unique
    canary value, (2) a changed `Location` header (redirect-style params), and
    (3) a syntax-breaker delta (error-based params, where the value is not
    reflected at all). Any one marks the parameter as a lead.
    """
    canary = canary or ("zzq" + secrets.token_hex(4))
    probe_url = _with_param(url, param, canary)
    ex_base, body_base = fetch(url, scope_checker=scope_checker, note="param baseline")
    loc_base = _location(ex_base)

    ex_p, body_p = fetch(probe_url, scope_checker=scope_checker, note="param probe")
    changed, why = response_changed(ex_base.status, body_base, ex_p.status, body_p, canary)
    if not changed:
        loc_p = _location(ex_p)
        if loc_p and loc_p != loc_base:
            changed, why = True, f"Location changed -> {loc_p[:48]}"

    if not changed:
        breaker_url = _with_param(url, param, "'")
        ex_b2, body_b2 = fetch(breaker_url, scope_checker=scope_checker, note="param breaker")
        c2, w2 = response_changed(ex_base.status, body_base, ex_b2.status, body_b2, "\x00")
        if c2:
            changed, why = True, f"breaker delta: {w2}"
    return changed, why, probe_url


def discover(urls, *, params=None, scope_checker=None, max_urls: int = 50,
             delay: float = 0.0) -> list[dict]:
    """Probe each URL for hidden params. Returns [{url,param,why,probe_url}]."""
    params = params or DEFAULT_PARAMS
    out: list[dict] = []
    for url in list(urls)[:max_urls]:
        for param in params:
            changed, why, probe_url = probe(url, param, scope_checker=scope_checker)
            if changed:
                out.append({"url": url, "param": param, "why": why, "probe_url": probe_url})
            if delay:
                time.sleep(delay)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Hidden-parameter discovery (GET-only fallback)")
    p.add_argument("--url", action="append", default=[], help="endpoint URL (repeatable)")
    p.add_argument("--list", help="file of endpoint URLs, one per line")
    p.add_argument("--out", help="write discovered param URLs (one per line)")
    p.add_argument("--scope-domain", action="append", default=[], help="allow-list (repeatable)")
    p.add_argument("--max-urls", type=int, default=50)
    p.add_argument("--delay", type=float, default=0.0)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    urls = list(args.url)
    if args.list and os.path.isfile(args.list):
        urls += [l.strip() for l in open(args.list) if l.strip()]

    scope_checker = None
    if args.scope_domain:
        from tools.scope_checker import ScopeChecker
        scope_checker = ScopeChecker(args.scope_domain)

    hits = discover(urls, scope_checker=scope_checker,
                    max_urls=args.max_urls, delay=args.delay)
    if args.json:
        import json
        print(json.dumps({"schema": "param-probe/1", "hits": hits}, indent=2))
    else:
        for h in hits:
            print(f"[PARAM] {h['url']} -> {h['param']}  ({h['why']})")
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as fh:
            fh.write("\n".join(h["probe_url"] for h in hits) + ("\n" if hits else ""))
    return 0 if hits else 4


if __name__ == "__main__":
    raise SystemExit(main())
