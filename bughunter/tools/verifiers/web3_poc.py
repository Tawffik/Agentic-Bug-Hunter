#!/usr/bin/env python3
"""Web3 PoC verifier — deterministic oracle via `forge test`.

A smart-contract lead is only confirmed when a Foundry test that demonstrates the
exploit actually passes. Static pattern hits (access-control, reentrancy, ...) are
LEADs; this verifier is the oracle: it runs `forge test --match-test <name> --json`
in the given project and confirms only on a passing test.

Finding fields:
  project_dir : path to a Foundry project (foundry.toml)
  test_name   : the exploit test to run (e.g. test_anyoneCanMint)

Honest: if forge is not installed or the test does not pass, this rejects/skips —
it never fabricates a confirmation.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess

from tools.verifiers.base import VerifyResult, confirmed, rejected, skipped

VULN_CLASS = "web3-poc"


def _walk_status(obj, needle):
    """Collect 'status' for any test key containing `needle`."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and needle in k and isinstance(v, dict) and "status" in v:
                found.append(str(v.get("status")))
            found += _walk_status(v, needle)
    elif isinstance(obj, list):
        for v in obj:
            found += _walk_status(v, needle)
    return found


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    project = finding.get("project_dir")
    test = finding.get("test_name")
    if not project or not test:
        return skipped(VULN_CLASS, "needs project_dir + test_name")
    if not os.path.isfile(os.path.join(project, "foundry.toml")):
        return skipped(VULN_CLASS, f"no foundry.toml in {project}")
    if shutil.which("forge") is None:
        return skipped(VULN_CLASS, "forge not installed")

    try:
        p = subprocess.run(
            ["forge", "test", "--match-test", str(test), "--json", "-vv"],
            cwd=project, capture_output=True, text=True, timeout=300,
        )
    except subprocess.TimeoutExpired:
        return rejected(VULN_CLASS, "forge test timed out", [])
    except Exception as exc:  # noqa: BLE001
        return rejected(VULN_CLASS, f"forge test error: {type(exc).__name__}", [])

    statuses = []
    try:
        statuses = _walk_status(json.loads(p.stdout or "{}"), str(test))
    except ValueError:
        statuses = []  # compile/test failure -> no JSON

    if any(s.lower() == "success" for s in statuses):
        return confirmed(
            VULN_CLASS,
            f"exploit PoC `{test}` passes under forge test",
            [],
            f"forge exit={p.returncode}; statuses={statuses}",
        )
    ev = (p.stderr or p.stdout or "").strip().splitlines()[-3:]
    return rejected(VULN_CLASS, f"PoC `{test}` did not pass", [],
                    " | ".join(ev)[:300])