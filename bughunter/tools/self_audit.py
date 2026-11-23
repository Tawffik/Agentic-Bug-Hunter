#!/usr/bin/env python3
"""Self-audit + continuous-evolution engine.

The agent should be able to inspect itself: what it can do, what is missing, and
whether a change broke anything. This tool:

  1. Inventories its own capabilities (tools, skills, agents, commands, tests,
     external binaries) from the repo — no hardcoded lists to rot.
  2. Detects coverage gaps (missing external tools, undocumented tools).
  3. Detects regressions: runs the test suite and compares to a stored baseline.
  4. Records improvements with measured before/after metrics in an append-only
     ledger, so upgrades are tracked rather than remembered.

Everything is read-only except `baseline` / `record`, which write under the
self-audit home (default: bughunter/memory/self-audit/).

Usage:
  python3 bughunter/tools/self_audit.py audit              # report
  python3 bughunter/tools/self_audit.py audit --json --run-tests
  python3 bughunter/tools/self_audit.py baseline            # record test baseline
  python3 bughunter/tools/self_audit.py drift               # regression gate (exit 1 on regression)
  python3 bughunter/tools/self_audit.py record --title "..." --metric tests_passed=1300 --note "..."
  python3 bughunter/tools/self_audit.py ledger
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../bughunter/tools
REPO = HERE.parents[1]                           # repo root
PKG = HERE.parent                                # .../bughunter
DEFAULT_HOME = PKG / "memory" / "self-audit"

_ARSENAL_LINE = re.compile(r'^\s*"([A-Za-z0-9_.+-]+)\|([a-z0-9_-]+)\|')
_README_TOOL = re.compile(r"\|\s*`([A-Za-z0-9_./-]+\.(?:py|sh))`")
_PYTEST_PASSED = re.compile(r"(\d+)\s+passed")
_PYTEST_FAILED = re.compile(r"(\d+)\s+failed")
_PYTEST_ERRORS = re.compile(r"(\d+)\s+error")
_PYTEST_SKIPPED = re.compile(r"(\d+)\s+skipped")

# Private helpers are not user-facing capabilities and are exempt from the
# "documented in README" check.
_TOOL_EXEMPT = {"__init__.py", "banner.py"}


def _is_cli_tool(path: Path) -> bool:
    """A user-facing capability has an entry point.

    Shell scripts and Python files with a ``__main__`` guard are runnable on
    their own and belong in the catalog; import-only Python modules are internal
    plumbing and are exempt (otherwise the gap report fills with noise).
    """
    if path.suffix == ".sh":
        return True
    try:
        return "__main__" in path.read_text(errors="ignore")
    except OSError:
        return False


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Capability inventory (pure; `which` injectable for tests)
# ---------------------------------------------------------------------------

def parse_arsenal(repo: Path) -> list[dict]:
    """Read ARSENAL_TOOLS entries from external_arsenal.sh."""
    path = repo / "bughunter" / "tools" / "external_arsenal.sh"
    tools: list[dict] = []
    if not path.is_file():
        return tools
    for line in path.read_text(errors="ignore").splitlines():
        m = _ARSENAL_LINE.match(line)
        if m:
            tools.append({"name": m.group(1), "category": m.group(2)})
    return tools


def _documented_tools(repo: Path) -> set[str]:
    readme = repo / "bughunter" / "tools" / "README.md"
    if not readme.is_file():
        return set()
    return {m.group(1) for m in _README_TOOL.finditer(readme.read_text(errors="ignore"))}


def agent_tool_wiring(repo: Path = REPO) -> dict:
    """Compare advertised agent tool backends with functions that exist.

    The ReAct agent once advertised 13 network tools while only 2 had a
    backend, so most of its capability silently returned TOOL UNAVAILABLE.
    Static AST parsing keeps this check independent of optional dependencies.
    """
    agent_path = repo / "bughunter" / "agent.py"
    hunt_path = repo / "bughunter" / "tools" / "hunt.py"
    if not agent_path.is_file() or not hunt_path.is_file():
        return {"agent_backends": 0, "agent_dead_tools": []}
    try:
        agent_tree = ast.parse(agent_path.read_text(encoding="utf-8", errors="replace"))
        hunt_tree = ast.parse(hunt_path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as exc:
        return {"agent_backends": 0,
                "agent_dead_tools": [{"tool": "<parse>", "backend": str(exc)}]}
    hunt_defs = {
        node.name for node in ast.walk(hunt_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    backends: dict[str, str] = {}
    for node in ast.walk(agent_tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "TOOL_BACKENDS" for t in node.targets):
            continue
        for key, value in zip(node.value.keys, node.value.values):
            if isinstance(key, ast.Constant) and isinstance(value, ast.Constant):
                backends[str(key.value)] = str(value.value)
    dead = [{"tool": tool, "backend": backend}
            for tool, backend in backends.items() if backend not in hunt_defs]
    return {"agent_backends": len(backends), "agent_dead_tools": dead}


def collect_inventory(repo: Path = REPO, which=shutil.which) -> dict:
    skills = sorted(p.parent.name for p in (repo / "skills").glob("*/SKILL.md"))
    commands = sorted(p.name for p in (repo / "commands").glob("*.md"))
    agents = sorted(p.stem for p in (repo / "bughunter" / "agents").glob("*.md"))
    tests = sorted(p.name for p in (repo / "tests").glob("test_*.py"))

    tool_files = []
    tools_dir = repo / "bughunter" / "tools"
    for p in sorted(tools_dir.glob("*")):
        if p.suffix in (".py", ".sh") and not p.name.startswith("_") \
                and p.name not in _TOOL_EXEMPT and _is_cli_tool(p):
            tool_files.append(p.name)

    arsenal = parse_arsenal(repo)
    installed, missing = [], []
    for t in arsenal:
        (installed if which(t["name"]) else missing).append(t)

    documented = _documented_tools(repo)
    undocumented = sorted(t for t in tool_files if t not in documented)

    return {
        "repo": str(repo),
        "skills": skills,
        "commands": commands,
        "agents": agents,
        "tests": tests,
        "tool_files": tool_files,
        "external_installed": installed,
        "external_missing": missing,
        "documented_tools": sorted(documented),
        "undocumented_tools": undocumented,
        **agent_tool_wiring(repo),
    }


# ---------------------------------------------------------------------------
# Gap analysis
# ---------------------------------------------------------------------------

def detect_gaps(inv: dict) -> list[dict]:
    gaps: list[dict] = []

    missing = inv.get("external_missing", [])
    if missing:
        by_cat: dict[str, list[str]] = {}
        for t in missing:
            by_cat.setdefault(t["category"], []).append(t["name"])
        for cat, names in sorted(by_cat.items()):
            gaps.append({
                "kind": "missing_external",
                "severity": "low" if cat in ("ai", "mobile") else "medium",
                "summary": f"{len(names)} missing '{cat}' tool(s) reduce coverage",
                "fix": "bash bughunter/tools/external_arsenal.sh --install-hint <tool>",
                "items": names,
            })

    dead = inv.get("agent_dead_tools", [])
    if dead:
        gaps.append({
            "kind": "dead_agent_tool",
            "severity": "high",
            "summary": f"{len(dead)} advertised agent tool(s) have no backend",
            "fix": "implement the hunt.py backend or remove the advertised tool",
            "items": [f"{d['tool']} -> {d['backend']}" for d in dead],
        })

    undoc = inv.get("undocumented_tools", [])
    if undoc:
        gaps.append({
            "kind": "undocumented_tool",
            "severity": "low",
            "summary": f"{len(undoc)} tool(s) are not listed in tools/README.md",
            "fix": "add a row to bughunter/tools/README.md",
            "items": undoc,
        })

    if not inv.get("tests"):
        gaps.append({"kind": "no_tests", "severity": "high",
                     "summary": "no tests found", "fix": "add tests/", "items": []})
    return gaps


def external_coverage(inv: dict) -> float:
    total = len(inv.get("external_installed", [])) + len(inv.get("external_missing", []))
    return len(inv.get("external_installed", [])) / total if total else 1.0


def documentation_ratio(inv: dict) -> float:
    files = inv.get("tool_files", [])
    if not files:
        return 1.0
    undocumented = set(inv.get("undocumented_tools", []))
    return (len(files) - len(undocumented)) / len(files)


# ---------------------------------------------------------------------------
# Test run + regression detection
# ---------------------------------------------------------------------------

def parse_pytest_summary(text: str) -> dict:
    def _n(pat, default=0):
        m = pat.search(text)
        return int(m.group(1)) if m else default

    passed = _n(_PYTEST_PASSED)
    failed = _n(_PYTEST_FAILED)
    errors = _n(_PYTEST_ERRORS)
    skipped = _n(_PYTEST_SKIPPED)
    return {
        "passed": passed, "failed": failed, "errors": errors, "skipped": skipped,
        "total": passed + failed + errors + skipped,
    }


def run_tests(repo: Path = REPO, timeout: int = 1800) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
            cwd=str(repo), capture_output=True, text=True, timeout=timeout,
        )
        summary = parse_pytest_summary(proc.stdout + "\n" + proc.stderr)
        summary["rc"] = proc.returncode
        return summary
    except subprocess.TimeoutExpired:
        return {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "total": 0,
                "rc": 124, "error": "pytest timed out"}
    except OSError as exc:
        return {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "total": 0,
                "rc": 127, "error": str(exc)}


def detect_regression(current: dict, baseline: dict | None) -> dict:
    if not baseline:
        return {"regression": False, "reason": "no baseline recorded"}
    if current.get("failed", 0) > baseline.get("failed", 0):
        return {"regression": True,
                "reason": f"failures rose {baseline.get('failed')} -> {current.get('failed')}"}
    if current.get("errors", 0) > baseline.get("errors", 0):
        return {"regression": True,
                "reason": f"errors rose {baseline.get('errors')} -> {current.get('errors')}"}
    if current.get("passed", 0) < baseline.get("passed", 0):
        return {"regression": True,
                "reason": f"passing tests dropped {baseline.get('passed')} -> {current.get('passed')}"}
    return {"regression": False, "reason": "at or above baseline"}


# ---------------------------------------------------------------------------
# Health score
# ---------------------------------------------------------------------------

def health_score(inv: dict, tests: dict | None) -> int:
    score = 0.0
    if tests and tests.get("total"):
        score += 50.0 * (tests.get("passed", 0) / tests["total"])
    else:
        score += 25.0  # unknown tests — neutral
    score += 20.0 * external_coverage(inv)
    score += 20.0 * documentation_ratio(inv)
    score += 10.0  # audit is being run now => fresh
    return int(round(score))


# ---------------------------------------------------------------------------
# Improvement ledger
# ---------------------------------------------------------------------------

def home_dir(override: str | None = None) -> Path:
    return Path(override) if override else DEFAULT_HOME


def ledger_path(home: Path) -> Path:
    return home / "improvements.jsonl"


def baseline_path(home: Path) -> Path:
    return home / "baseline.json"


def _write_owner_only(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)


def read_ledger(home: Path) -> list[dict]:
    path = ledger_path(home)
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def record_improvement(home: Path, title: str, metrics: dict, note: str = "") -> dict:
    rows = read_ledger(home)
    previous = rows[-1].get("metrics", {}) if rows else {}
    deltas = {}
    for key, value in metrics.items():
        if isinstance(value, (int, float)) and isinstance(previous.get(key), (int, float)):
            deltas[key] = value - previous[key]
    entry = {
        "ts": _now(),
        "title": title,
        "metrics": metrics,
        "deltas": deltas,
        "note": note,
    }
    path = ledger_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, separators=(",", ":")) + "\n")
    return entry


def read_baseline(home: Path) -> dict | None:
    path = baseline_path(home)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def write_baseline(home: Path, tests: dict) -> dict:
    record = {"ts": _now(), **tests}
    _write_owner_only(baseline_path(home), json.dumps(record, indent=2) + "\n")
    return record


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_metrics(pairs: list[str]) -> dict:
    metrics: dict = {}
    for pair in pairs or []:
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        value = value.strip()
        try:
            metrics[key.strip()] = int(value)
            continue
        except ValueError:
            pass
        try:
            metrics[key.strip()] = float(value)
            continue
        except ValueError:
            metrics[key.strip()] = value
    return metrics


def cmd_audit(args, home: Path) -> int:
    inv = collect_inventory(REPO)
    gaps = detect_gaps(inv)
    tests = run_tests(REPO) if args.run_tests else None
    drift = None
    if tests is not None:
        drift = detect_regression(tests, read_baseline(home))
    report = {
        "ts": _now(),
        "health_score": health_score(inv, tests),
        "capabilities": {
            "skills": len(inv["skills"]),
            "commands": len(inv["commands"]),
            "agents": len(inv["agents"]),
            "tools": len(inv["tool_files"]),
            "tests": len(inv["tests"]),
            "external_installed": len(inv["external_installed"]),
            "external_missing": len(inv["external_missing"]),
            "agent_backends": inv.get("agent_backends", 0),
            "agent_dead_tools": len(inv.get("agent_dead_tools", [])),
        },
        "gaps": gaps,
        "tests": tests,
        "drift": drift,
    }
    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    cap = report["capabilities"]
    print(f"Self-audit — health {report['health_score']}/100")
    print(f"  skills {cap['skills']} | commands {cap['commands']} | agents {cap['agents']} "
          f"| tools {cap['tools']} | tests {cap['tests']}")
    print(f"  external tools: {cap['external_installed']} installed, "
          f"{cap['external_missing']} missing")
    print(f"  agent tool backends: {cap['agent_backends']} wired, "
          f"{cap['agent_dead_tools']} dead")
    if tests:
        print(f"  tests: {tests.get('passed')} passed, {tests.get('failed')} failed, "
              f"{tests.get('errors')} errors")
    if drift:
        flag = "REGRESSION" if drift["regression"] else "clean"
        print(f"  drift: {flag} — {drift['reason']}")
    if gaps:
        print("\nGaps:")
        for g in gaps:
            print(f"  [{g['severity']}] {g['summary']}")
            print(f"        fix: {g['fix']}")
    else:
        print("\nNo gaps detected.")
    return 0


def cmd_baseline(args, home: Path) -> int:
    tests = run_tests(REPO)
    rec = write_baseline(home, tests)
    print(f"[+] baseline recorded: {rec['passed']} passed, {rec['failed']} failed "
          f"-> {baseline_path(home)}")
    return 1 if (tests.get("failed") or tests.get("errors")) else 0


def cmd_drift(args, home: Path) -> int:
    tests = run_tests(REPO)
    baseline = read_baseline(home)
    drift = detect_regression(tests, baseline)
    if baseline is None:
        print("[!] no baseline — run: self_audit.py baseline")
        return 0
    print(f"current:  {tests.get('passed')} passed, {tests.get('failed')} failed")
    print(f"baseline: {baseline.get('passed')} passed, {baseline.get('failed')} failed")
    if drift["regression"]:
        print(f"[-] REGRESSION: {drift['reason']}")
        return 1
    print(f"[+] no regression — {drift['reason']}")
    return 0


def cmd_record(args, home: Path) -> int:
    metrics = _parse_metrics(args.metric)
    entry = record_improvement(home, args.title, metrics, note=args.note or "")
    print(f"[+] recorded: {entry['title']}")
    if entry["deltas"]:
        print("    deltas: " + ", ".join(f"{k} {'+' if v >= 0 else ''}{v}" for k, v in entry["deltas"].items()))
    return 0


def cmd_ledger(args, home: Path) -> int:
    rows = read_ledger(home)
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    if not rows:
        print("[.] no improvements recorded yet")
        return 0
    for row in rows:
        print(f"{row['ts']}  {row['title']}")
        if row.get("deltas"):
            print("    " + ", ".join(f"{k} {'+' if v >= 0 else ''}{v}" for k, v in row["deltas"].items()))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Self-audit + continuous-evolution engine.")
    ap.add_argument("--home", default=None, help=f"self-audit data dir (default: {DEFAULT_HOME})")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("audit", help="capability inventory + gaps (+ optional tests/drift)")
    pa.add_argument("--json", action="store_true")
    pa.add_argument("--run-tests", action="store_true", help="also run the suite and check drift")

    sub.add_parser("baseline", help="record current test results as the regression baseline")
    sub.add_parser("drift", help="run tests and compare to baseline (exit 1 on regression)")

    pr = sub.add_parser("record", help="append an improvement with measured metrics")
    pr.add_argument("--title", required=True)
    pr.add_argument("--metric", action="append", default=[], help="key=value (repeatable)")
    pr.add_argument("--note", default="")

    pl = sub.add_parser("ledger", help="show recorded improvements")
    pl.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)
    home = home_dir(args.home)
    return {
        "audit": cmd_audit,
        "baseline": cmd_baseline,
        "drift": cmd_drift,
        "record": cmd_record,
        "ledger": cmd_ledger,
    }[args.cmd](args, home)


if __name__ == "__main__":
    raise SystemExit(main())
