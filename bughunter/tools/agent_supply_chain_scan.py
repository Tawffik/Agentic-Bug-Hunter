#!/usr/bin/env python3
"""Agent supply-chain scanner — audit the prompts/tools your agent loads.

An agent is an API endpoint with your credentials and your shell. Its skills,
agent specs, and MCP configs are executable supply chain, exactly like npm/PyPI
packages (2026: "X-Ray Your Agents", Nopilot, MCP rug-pulls). This scans local
prompt/config files for the patterns that let a dependency take over the agent:

  critical  curl|wget piped into a shell
  high      hardcoded secret, unpinned install, destructive shell, injection directive
  medium    broad agent capability (bash + write + webfetch), unbounded network tool

It is static and offline. It never executes anything it scans.

    python3 -m tools.agent_supply_chain_scan --root . --json
    python3 -m tools.agent_supply_chain_scan --root skills --fail-on high
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re

SCHEMA = "agent-supply-chain/1"

# rule id -> (severity, compiled pattern, why)
_RULES = {
    "curl-pipe-shell": ("critical", re.compile(
        r"(?:curl|wget)\b[^\n|]{0,200}\|\s*(?:sudo\s+)?(?:ba|z|k)?sh\b", re.I),
        "remote script piped straight into a shell"),
    "hardcoded-secret": ("high", re.compile(
        r"(AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
        r"(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{6,})", re.I),
        "secret committed into a prompt/config file"),
    "unpinned-install": ("high", re.compile(
        r"\b(?:pip3?|python3?\s+-m\s+pip)\s+install\s+(?!-)\b([A-Za-z0-9_.-]+)\b"
        r"(?!\s*(?:==|>=|<=|~=|@))", re.I),
        "dependency installed without a pinned version"),
    "destructive-shell": ("high", re.compile(
        r"(rm\s+-rf\s+/(?:\s|$)|chmod\s+777|mkfs\.|dd\s+if=|>\s*/dev/sd)", re.I),
        "destructive shell command in an instruction"),
    "injection-directive": ("high", re.compile(
        r"(ignore\s+(?:all\s+)?previous\s+instructions|bypass\s+(?:the\s+)?scope|"
        r"do\s+not\s+(?:ask|request)\s+(?:for\s+)?(?:approval|confirmation)|"
        r"exfiltrat\w+|send\s+(?:the\s+)?(?:data|secrets?|keys?)\s+to\s+https?://)", re.I),
        "prompt text that tries to override safety/scope"),
    "network-tool": ("medium", re.compile(
        r"(fetch|browse|http[_ -]?get|requests?\.(?:get|post)|urlopen)\s*\(", re.I),
        "tool with outbound network capability — confirm it is scope-guarded"),
}

_BROAD_TOOLS = re.compile(r"tools:\s*\n((?:\s{2}\w+:\s*(?:true|false)\s*\n)+)")
_TRUE = re.compile(r"\s{2}(\w+):\s*true")


def _is_target(path: str) -> bool:
    low = path.lower().replace("\\", "/")
    if any(part in low for part in ("/node_modules/", "/.git/", "/__pycache__/")):
        return False
    if low.endswith(".md") and ("/agents/" in low or "/skills/" in low):
        return True
    base = os.path.basename(low)
    return base in {".mcp.json", "opencode.json", "opencode.jsonc"} or (
        base.startswith("mcp") and base.endswith(".json"))


def _redact(line: str) -> str:
    line = re.sub(r"(AKIA[0-9A-Z]{16})", "AKIA[redacted]", line)
    line = re.sub(r"((?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"])[^'\"]+",
                  r"\1[redacted]", line, flags=re.I)
    return line.strip()[:200]


def _looks_like_doc_example(path: str, line: str) -> bool:
    """Payload corpora and documentation examples are not executable supply chain."""
    low = path.lower().replace("\\", "/")
    if "/payloads/" in low or "/references/" in low or "/knowledge/" in low:
        return True
    s = line.strip().lower()
    if s.startswith(("-", "*", ">", "#", "|", "`")):
        return True
    return any(w in s for w in ("example", "pattern", "e.g.", "attacker pr", "etc.",
                                "dangerous", "$attacker"))


def _iter_files(root: str):
    for path in glob.glob(os.path.join(root, "**", "*"), recursive=True):
        if os.path.isfile(path) and _is_target(path):
            yield path


def scan(root: str) -> dict:
    findings = []
    files = 0
    for path in _iter_files(root):
        files += 1
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        lines = text.splitlines()
        for rule, (sev, rx, why) in _RULES.items():
            for m in rx.finditer(text):
                line_no = text.count("\n", 0, m.start()) + 1
                snippet = _redact(lines[line_no - 1]) if line_no <= len(lines) else ""
                if rule in ("curl-pipe-shell", "destructive-shell") and \
                        _looks_like_doc_example(path, lines[line_no - 1] if line_no <= len(lines) else ""):
                    continue
                findings.append({"rule": rule, "severity": sev, "path": path,
                                 "line": line_no, "snippet": snippet, "why": why})
        # Broad capability is a frontmatter shape, not a single line.
        block = _BROAD_TOOLS.search(text)
        if block:
            enabled = set(_TRUE.findall(block.group(1)))
            if {"bash", "write", "webfetch"} <= enabled:
                findings.append({"rule": "broad-agent-capability", "severity": "medium",
                                 "path": path, "line": 1,
                                 "snippet": "tools: bash+write+webfetch all enabled",
                                 "why": "agent can run, write and fetch — verify least privilege"})

    order = {"critical": 0, "high": 1, "medium": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 9), f["path"], f["line"]))
    counts = {"critical": 0, "high": 0, "medium": 0}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    return {"schema": SCHEMA, "root": root, "files_scanned": files,
            "counts": counts, "findings": findings}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Scan agent skills/configs as a supply chain")
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on", choices=["critical", "high", "medium"], default=None)
    args = ap.parse_args(argv)

    out = scan(args.root)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"[+] scanned {out['files_scanned']} files — "
              f"{out['counts']['critical']} critical, {out['counts']['high']} high, "
              f"{out['counts']['medium']} medium")
        for f in out["findings"]:
            print(f"  [{f['severity']}] {f['rule']} {f['path']}:{f['line']} — {f['why']}")
    if args.fail_on:
        rank = {"medium": 0, "high": 1, "critical": 2}[args.fail_on]
        worst = {"medium": 0, "high": 1, "critical": 2}
        if any(worst.get(f["severity"], 0) >= rank for f in out["findings"]):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
