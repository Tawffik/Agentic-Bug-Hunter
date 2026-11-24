#!/usr/bin/env python3
"""Parse ffuf JSON output into plain URLs.

`recon_engine.sh` writes content-discovery results to `dirs/ffuf_<host>.json`
but nothing ever reads them, so every fuzzed path that isn't already in a crawl
output is silently dropped and never becomes a lead. This closes that loop.

Usage:
  python3 -m tools.parse_ffuf dirs/ffuf_*.json              # URLs to stdout
  python3 -m tools.parse_ffuf dirs/ffuf_a.json dirs/ffuf_b.json
  python3 -m tools.parse_ffuf --json dirs/ffuf_a.json       # {"urls": [...]}
"""
from __future__ import annotations

import argparse
import json
import sys


def urls_from_ffuf(data: dict) -> list[str]:
    """Extract absolute URLs from one parsed ffuf JSON document."""
    out: list[str] = []
    base = ""
    cfg = data.get("config") or {}
    if isinstance(cfg.get("url"), str):
        base = cfg["url"]
    for r in data.get("results") or []:
        # Preferred: ffuf already wrote the full URL.
        url = r.get("url")
        if not url:
            fuzz = ((r.get("input") or {}).get("FUZZ")
                    or (r.get("input") or {}).get("fuzz") or "")
            if base and fuzz:
                url = base.replace("FUZZ", str(fuzz))
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            out.append(url)
    return out


def urls_from_files(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for p in paths:
        try:
            with open(p, errors="replace") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        for u in urls_from_ffuf(data if isinstance(data, dict) else {}):
            if u not in seen:
                seen.add(u)
                out.append(u)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="ffuf JSON -> URL list")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    urls = urls_from_files(args.files)
    if args.json:
        print(json.dumps({"urls": urls}))
    else:
        print("\n".join(urls))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
