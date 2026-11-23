#!/usr/bin/env python3
"""Fuzz response-diff — classify ffuf hits against each host's own baseline.

Adapted from the "smart fuzzing" response-diff idea (BugBountyCI / Zero Track):
a fuzzing hit is a *signal*, not a vulnerability, and a status code alone is not
a signal. The right question is "how does this differ from what this host
returns for a path that does not exist?"

Without this, content discovery floods the lead board: an SPA or an
edge/WAF catch-all returns 200 for every path, so every fuzzed word looks like
a hit. (This mirrors the real superdrug.com run where a baseline-matching bug
produced 21/21 INTERESTING hits — statistically implausible.)

Per host:
  baseline = response to a random, almost-certainly-nonexistent path
  classify(hit) = compare the hit to THAT host's baseline (exact host match —
                  never another host's, which is the bug that caused the 21/21)

Labels are observational and NEVER "vulnerability":
  SPA_FALLBACK  content fingerprint identical to the catch-all baseline
  DUPLICATE     same (status, length) already seen on this host (repeat block page)
  NOISE         status/content-type/length all ~= baseline
  AUTH_REQUIRED status 401/407 vs baseline
  REDIRECT      3xx vs baseline
  SERVER_ERROR  5xx vs baseline
  WAF_BLOCK     403/406/429 immediately after a 2xx baseline
  INTERESTING   status/content-type/length meaningfully differs
  UNKNOWN       no baseline for this exact host — we do not guess

Usage:
  python3 -m tools.fuzz_diff --ffuf-dir recon/t/dirs --baseline-out /tmp/b.json
  python3 -m tools.fuzz_diff --baseline-json /tmp/b.json --ffuf-dir recon/t/dirs --json
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import secrets
import sys
from urllib.parse import urlsplit

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools.verifiers.base import fetch  # noqa: E402

_SIGNAL_LABELS = {"INTERESTING", "AUTH_REQUIRED", "REDIRECT", "SERVER_ERROR", "WAF_BLOCK"}


def fingerprint(body: bytes) -> str:
    normalized = re.sub(rb"\d+", b"", body or b"")
    return hashlib.md5(normalized).hexdigest()


def normalize_host(url: str) -> str | None:
    parts = urlsplit(url or "")
    if not parts.scheme or not parts.netloc:
        return None
    return f"{parts.scheme}://{parts.netloc}"


def classify(hit: dict, base: dict | None, body_available: bool = False) -> tuple[str, str]:
    """Classify one hit against its own host's baseline. Pure (unit-tested)."""
    if base is None:
        return "UNKNOWN", "no exact-host baseline match available"
    if body_available and hit.get("fingerprint") and hit["fingerprint"] == base.get("fingerprint"):
        return "SPA_FALLBACK", "identical content fingerprint to baseline (catch-all)"

    def _i(v):
        try:
            return int(v) if v is not None else None
        except (TypeError, ValueError):
            return None

    s, bs = _i(hit.get("status")), _i(base.get("status"))
    if s is not None and s != bs:
        if s in (401, 407):
            return "AUTH_REQUIRED", f"status {s} != baseline {base.get('status')} (auth challenge)"
        if s in (301, 302, 303, 307, 308):
            loc = (hit.get("location") or "")[:120]
            return "REDIRECT", f"status {s} != baseline {base.get('status')}" + (f" loc={loc}" if loc else "")
        if s in (500, 502, 503, 504):
            return "SERVER_ERROR", f"status {s} != baseline {base.get('status')}"
        if s in (403, 406, 429, 493):
            if bs is not None and 200 <= bs < 300:
                return "WAF_BLOCK", f"status {s} after baseline {base.get('status')}"
            return "INTERESTING", f"status {s} != baseline {base.get('status')}"

    # Same status: compare content-type and length band.
    ct, bct = (hit.get("content_type") or ""), (base.get("content_type") or "")
    bl, hl = base.get("length") or 0, hit.get("length") or 0
    if ct and bct and ct.split(";")[0] != bct.split(";")[0]:
        return "INTERESTING", f"content-type {ct.split(';')[0]} != baseline {bct.split(';')[0]}"
    band = max(16, int(0.05 * max(bl, 1)))
    if abs(hl - bl) > band:
        return "INTERESTING", f"length {hl} vs baseline {bl}"
    return "NOISE", f"~= baseline (status {s}, length {hl}~{bl})"


def dedupe_signals(classified: list[dict]) -> list[dict]:
    """Within a host, collapse repeated (status,length) signals (repeat block pages)."""
    seen: dict[str, set] = {}
    out = []
    for c in classified:
        host = normalize_host(c.get("url", "")) or ""
        if c["label"] not in _SIGNAL_LABELS:
            out.append(c)
            continue
        sig = (c.get("status"), c.get("length"))
        if sig in seen.setdefault(host, set()):
            c = {**c, "label": "DUPLICATE", "reason": "same (status, length) already seen on this host"}
        else:
            seen[host].add(sig)
        out.append(c)
    return out


def build_baseline(hosts: list[str], *, scope_checker=None, timeout: float = 8.0,
                   max_hosts: int = 50) -> dict:
    """Probe a random nonexistent path on each host -> per-host baseline."""
    base: dict[str, dict] = {}
    for host in hosts[:max_hosts]:
        if not host.startswith(("http://", "https://")):
            host = "https://" + host
        probe = host.rstrip("/") + f"/__zzq_nonexistent_{secrets.token_hex(4)}__"
        ex, body = fetch(probe, scope_checker=scope_checker, timeout=timeout,
                         note="fuzz-diff baseline")
        norm = normalize_host(host)
        if norm and ex.status is not None:
            base[norm] = {
                "status": ex.status, "length": len(body),
                "content_type": (ex.response_headers.get("Content-Type")
                                 or ex.response_headers.get("content-type") or ""),
                "fingerprint": fingerprint(body),
            }
    return base


def load_ffuf_hits(paths: list[str]) -> list[dict]:
    hits = []
    for p in paths:
        try:
            data = json.load(open(p, errors="replace"))
        except (OSError, ValueError):
            continue
        for r in (data.get("results") or []):
            url = r.get("url")
            if not url:
                fuzz = (r.get("input") or {}).get("FUZZ", "")
                base = (data.get("config") or {}).get("url", "")
                if base and fuzz:
                    url = base.replace("FUZZ", str(fuzz))
            if not url:
                continue
            hits.append({
                "url": url, "status": r.get("status"), "length": r.get("length"),
                "content_type": r.get("content-type") or r.get("content_type") or "",
                "location": (r.get("redirectlocation") or r.get("location") or ""),
            })
    return hits


def diff(baseline: dict, hits: list[dict], body_available: bool = False) -> list[dict]:
    classified = []
    for h in hits:
        base = baseline.get(normalize_host(h["url"]) or "")
        label, reason = classify(h, base, body_available)
        classified.append({**h, "label": label, "reason": reason})
    return dedupe_signals(classified)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Classify ffuf hits vs per-host baseline")
    p.add_argument("--ffuf-dir", help="dir of ffuf json files")
    p.add_argument("--ffuf-json", action="append", default=[], help="ffuf json file (repeatable)")
    p.add_argument("--hosts", help="file of hosts to baseline (default: hosts from ffuf hits)")
    p.add_argument("--baseline-json", help="existing baseline.json (skip probing)")
    p.add_argument("--baseline-out", help="write baseline here")
    p.add_argument("--scope-domain", action="append", default=[])
    p.add_argument("--out", help="write signal URLs here")
    p.add_argument("--include-unknown", action="store_true",
                   help="also write UNKNOWN (no baseline) URLs — safe default for recon")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    paths = list(args.ffuf_json)
    if args.ffuf_dir:
        paths += glob.glob(os.path.join(args.ffuf_dir, "*.json"))
    hits = load_ffuf_hits(paths)

    if args.baseline_json and os.path.isfile(args.baseline_json):
        baseline = json.load(open(args.baseline_json))
    else:
        hosts = []
        if args.hosts and os.path.isfile(args.hosts):
            hosts = [l.strip() for l in open(args.hosts) if l.strip()]
        else:
            seen, hosts = set(), []
            for h in hits:
                nh = normalize_host(h["url"])
                if nh and nh not in seen:
                    seen.add(nh)
                    hosts.append(nh)
        scope_checker = None
        if args.scope_domain:
            from tools.scope_checker import ScopeChecker
            scope_checker = ScopeChecker(args.scope_domain)
        baseline = build_baseline(hosts, scope_checker=scope_checker)
        if args.baseline_out:
            os.makedirs(os.path.dirname(os.path.abspath(args.baseline_out)), exist_ok=True)
            json.dump(baseline, open(args.baseline_out, "w"), indent=2)

    results = diff(baseline, hits)
    keep = set(_SIGNAL_LABELS) | ({"UNKNOWN"} if args.include_unknown else set())
    interesting = [r["url"] for r in results if r["label"] in keep]
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        open(args.out, "w").write("\n".join(interesting) + ("\n" if interesting else ""))
    if args.json:
        print(json.dumps({"schema": "fuzz-diff/1", "baseline_hosts": len(baseline),
                          "hits": len(hits), "interesting": len(interesting),
                          "results": results}, indent=2))
    else:
        from collections import Counter
        print(f"baseline hosts: {len(baseline)} | hits: {len(hits)} | signals: {len(interesting)}")
        print("labels:", dict(Counter(r["label"] for r in results)))
        for r in results:
            if r["label"] in _SIGNAL_LABELS:
                print(f"  [{r['label']}] {r['url']}  ({r['reason']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
