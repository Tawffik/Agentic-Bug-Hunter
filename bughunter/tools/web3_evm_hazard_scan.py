#!/usr/bin/env python3
"""Bounded EVM hazard scanner — LEAD-only signals for patterns generic linters miss.

Checks:
  1. payable multicall / batch loop reusing msg.value (SushiSwap Trident class)
  2. msg.value read inside a loop in any payable function
  3. L2 execution-dialect hazards (Arbitrum block.number, zkSync EOA checks,
     OP-stack balance sweeps, prevrandao/difficulty, coinbase)

Every hit is a LEAD. Read the function, prove reachability, and reproduce with a
Foundry test before treating it as a finding. No network access, no execution.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "lib", "libs", "out", "cache", "artifacts",
    "broadcast", "coverage", "test", "tests", "script", "scripts",
}

MULTICALL_NAMES = {
    "multicall", "multicallbytes", "multicallvalue", "batch", "batchcall",
    "aggregate", "aggregatevalue", "executebatch", "executebatchvalue",
}

L2_CHECKS = [
    ("L2-ARB-01", "arbitrum", re.compile(r"\bblock\.number\b"),
     "Arbitrum exposes the L1 block number; short L2 windows desync."),
    ("L2-ZKSYNC-01", "zksync", re.compile(r"\bextcodesize\s*\(|\btx\.origin\s*==\s*msg\.sender\b"),
     "EOA-vs-contract checks break native account abstraction on zkSync Era."),
    ("L2-OP-01", "optimism", re.compile(r"\baddress\s*\(\s*this\s*\)\s*\.balance\b"),
     "Exact balance sweeps can revert on OP Stack when L1 data fees are deducted."),
    ("L2-RAND-01", "all-l2", re.compile(r"\bblock\.(prevrandao|difficulty)\b"),
     "prevrandao/difficulty is sequencer-controlled or constant on L2 rollups."),
    ("L2-COINBASE-01", "all-l2", re.compile(r"\bblock\.coinbase\b"),
     "coinbase is the sequencer fee vault on L2, not a block builder."),
]


@dataclass
class Finding:
    rule: str
    severity: str
    file: str
    line: int
    snippet: str
    signal: str
    verify: str


def strip_comments(text: str) -> str:
    """Remove // and /* */ comments while preserving newlines and line numbers."""
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def function_blocks(text: str):
    """Yield (name, signature, body, start_line) for Solidity function blocks."""
    pattern = re.compile(r"\bfunction\s+([A-Za-z_]\w*)\s*\(([^)]*)\)([^{;]*)\{", re.S)
    for match in pattern.finditer(text):
        body_start = match.end() - 1
        depth = 0
        for idx in range(body_start, len(text)):
            if text[idx] == "{":
                depth += 1
            elif text[idx] == "}":
                depth -= 1
                if depth == 0:
                    body = text[body_start + 1:idx]
                    line = text[:match.start()].count("\n") + 1
                    yield match.group(1), match.group(2) + match.group(3), body, line
                    break


def first_loop_with(body: str, needle: re.Pattern[str]) -> bool:
    for loop in re.finditer(r"\b(?:for|while)\s*\(", body):
        brace = body.find("{", loop.end())
        if brace == -1:
            continue
        depth = 0
        for idx in range(brace, len(body)):
            if body[idx] == "{":
                depth += 1
            elif body[idx] == "}":
                depth -= 1
                if depth == 0:
                    if needle.search(body[loop.start():idx + 1]):
                        return True
                    break
    return False


def scan_file(path: Path, root: Path, chains: set[str]) -> list[Finding]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    text = strip_comments(raw)
    rel = str(path.relative_to(root))
    findings: list[Finding] = []
    lines = text.splitlines()

    for name, signature, body, start_line in function_blocks(text):
        if "payable" not in signature:
            continue
        lname = name.lower()
        has_loop = bool(re.search(r"\b(?:for|while)\s*\(", body))
        has_value = bool(re.search(r"\bmsg\.value\b", body))
        has_delegate = bool(re.search(r"\bdelegatecall\b", body))

        if lname in MULTICALL_NAMES and has_loop and (has_value or has_delegate):
            findings.append(Finding(
                "PAYABLE_MULTICALL_LOOP", "lead", rel, start_line,
                _snippet(lines, start_line),
                f"`{name}()` is payable and loops with msg.value/delegatecall; a single "
                "deposit can be reused across sub-actions.",
                "Prove one call reuses msg.value or performs N delegatecalls for one payment; PoC with Foundry.",
            ))
        elif has_loop and first_loop_with(body, re.compile(r"\bmsg\.value\b")):
            findings.append(Finding(
                "MSG_VALUE_IN_LOOP", "lead", rel, start_line,
                _snippet(lines, start_line),
                f"`{name}()` reads msg.value inside a loop; every iteration sees the full value.",
                "Check whether the loop forwards/spends msg.value more than once; PoC the excess.",
            ))

    for rule, chain, pattern, signal in L2_CHECKS:
        if chains and chain not in chains and "all-l2" not in chains:
            continue
        for match in pattern.finditer(text):
            line = text[:match.start()].count("\n") + 1
            findings.append(Finding(
                rule, "lead", rel, line, _snippet(lines, line),
                f"{signal} Matched: `{match.group(0).strip()}`.",
                "Confirm the deployment chain and whether the quirk changes the accounting/security path.",
            ))
            break
    return findings


def _snippet(lines: list[str], line: int) -> str:
    if 1 <= line <= len(lines):
        return lines[line - 1].strip()[:200]
    return ""


def iter_sol_files(root: Path):
    for path in sorted(root.rglob("*.sol")):
        if any(part.lower() in SKIP_DIRS for part in path.parts):
            continue
        yield path


def render_markdown(findings: list[Finding], root: Path) -> str:
    out = [
        "# Web3 EVM Hazard Scan (LEAD-only)",
        "",
        f"Root: `{root}`",
        f"Leads: **{len(findings)}**",
        "",
        "> Every row is a lead, not a finding. Prove reachability and reproduce before reporting.",
        "",
    ]
    if not findings:
        out.append("No matching signals.")
        return "\n".join(out) + "\n"
    out += ["| Rule | Location | Signal | Verify |", "|---|---|---|---|"]
    for item in findings:
        out.append(
            f"| `{item.rule}` | `{item.file}:{item.line}` | {item.signal.replace('|', '\\|')} | {item.verify} |"
        )
    out += ["", "## Matched lines", ""]
    for item in findings:
        out += [f"### {item.rule} — {item.file}:{item.line}", "", "```solidity", item.snippet, "```", ""]
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", help="Project root or a Solidity file")
    parser.add_argument("--chain", action="append", default=[],
                        choices=["arbitrum", "optimism", "zksync", "all-l2"],
                        help="Limit L2 checks (repeatable); default all")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--output", help="Write output to this file")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        parser.error(f"target not found: {target}")

    root = target if target.is_dir() else target.parent
    files = list(iter_sol_files(target)) if target.is_dir() else [target]
    if not files:
        parser.error("no .sol files found")

    chains = set(args.chain)
    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(path, root, chains))

    if args.json:
        payload = json.dumps([asdict(item) for item in findings], indent=2)
    else:
        payload = render_markdown(findings, root)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
        print(f"[+] {len(findings)} lead(s) written to {args.output}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
