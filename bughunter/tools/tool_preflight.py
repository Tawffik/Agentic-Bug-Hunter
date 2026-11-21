#!/usr/bin/env python3
"""tool_preflight.py — catch wrong/shadowed tool binaries before a hunt.

Born from a real failure: on the TikTok engagement, `httpx` on PATH was the
**Python** `httpx` client, not ProjectDiscovery's `httpx`. recon_engine.sh only
checks `command -v httpx`, so the live-host phase silently misfired and recon
yielded nothing — a failure mode that looks like "the target is small" instead
of "our tool is broken".

This preflight verifies that each required binary is the expected
implementation by inspecting its version banner, and reports:
  OK           expected marker present (e.g. "projectdiscovery")
  WRONG_BINARY a known shadow/anti-marker is present (e.g. "httpx[cli]")
  UNKNOWN      present but the expected marker is absent
  MISSING      not on PATH
  ERROR        the version probe itself failed

Exits non-zero when a tool is WRONG_BINARY (the dangerous silent case); pass
--strict to also fail on MISSING/UNKNOWN.

Usage:
  python3 bughunter/tools/tool_preflight.py
  python3 bughunter/tools/tool_preflight.py --json
  python3 bughunter/tools/tool_preflight.py --tools httpx,nuclei --strict
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys

# (tool, required marker, forbidden markers that reveal a shadowing binary).
# An empty marker means "present is enough" (some tools don't print the org);
# httpx carries an identity marker because its name collides with the Python
# `httpx` client, which is the exact shadow we were bitten by.
DEFAULT_TOOLS = [
    ("httpx", "projectdiscovery", ["could not run", "httpx[cli]", "pip install"]),
    ("nuclei", "", []),
    ("subfinder", "", []),
    ("katana", "", []),
    ("dnsx", "", []),
    ("naabu", "", []),
]

_BAD = {"WRONG_BINARY"}


def verify_tool(name: str, marker: str, forbidden: list[str], *,
                which=shutil.which, run=subprocess.run) -> dict:
    path = which(name)
    if not path:
        return {"tool": name, "status": "MISSING", "path": "", "detail": ""}
    try:
        proc = run([name, "-version"], capture_output=True, text=True, timeout=10)
        out = (proc.stdout or "") + (proc.stderr or "")
    except Exception as exc:  # noqa: BLE001 - any probe failure => ERROR
        return {"tool": name, "status": "ERROR", "path": path, "detail": str(exc)[:100]}
    low = out.lower()
    for bad in forbidden:
        if bad.lower() in low:
            return {"tool": name, "status": "WRONG_BINARY", "path": path,
                    "detail": f"shadowed binary ({bad})"}
    if not marker or marker.lower() in low:
        return {"tool": name, "status": "OK", "path": path, "detail": ""}
    return {"tool": name, "status": "UNKNOWN", "path": path,
            "detail": out.strip().splitlines()[0][:90] if out.strip() else "no version output"}


def preflight(tools=None, *, which=shutil.which, run=subprocess.run) -> list[dict]:
    tools = tools or DEFAULT_TOOLS
    return [verify_tool(n, m, f, which=which, run=run) for n, m, f in tools]


def _exit_code(results: list[dict], strict: bool) -> int:
    if any(r["status"] in _BAD for r in results):
        return 1
    if strict and any(r["status"] in ("MISSING", "UNKNOWN", "ERROR") for r in results):
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Verify required tools are the expected binaries.")
    ap.add_argument("--tools", default="", help="comma list to check (default: core recon set)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="also fail on MISSING/UNKNOWN/ERROR")
    ap.add_argument("--quiet", action="store_true", help="only print problems")
    args = ap.parse_args(argv)

    tools = DEFAULT_TOOLS
    if args.tools:
        wanted = {t.strip() for t in args.tools.split(",") if t.strip()}
        tools = [t for t in DEFAULT_TOOLS if t[0] in wanted] or [
            (t, "projectdiscovery", []) for t in sorted(wanted)]

    results = preflight(tools)
    code = _exit_code(results, args.strict)

    if args.json:
        print(json.dumps({"results": results, "ok": code == 0}, indent=2))
        return code

    for r in results:
        if args.quiet and r["status"] == "OK":
            continue
        icon = {"OK": "ok ", "MISSING": "!! ", "WRONG_BINARY": "XX ",
                "UNKNOWN": "?  ", "ERROR": "!! "}.get(r["status"], "?  ")
        line = f"{icon}{r['tool']:<10} {r['status']:<13} {r['path']}"
        if r["detail"]:
            line += f"  — {r['detail']}"
        print(line)
    if any(r["status"] == "WRONG_BINARY" for r in results):
        print("\n[!] A required tool is the WRONG binary (shadowed). Fix PATH "
              "(prepend ~/go/bin) or install the real tool before hunting.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
