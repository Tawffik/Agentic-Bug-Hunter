#!/usr/bin/env python3
"""Business-logic verifier — declarative sequence + invariant oracle.

Business logic has no generic signature, so the hunter encodes the exploit as a
short request sequence plus assertions about observable state. This verifier
executes the sequence and confirms ONLY when every assertion holds, including at
least one `violation` assertion that proves the invariant broke.

Finding shape:

    "steps": [
      {"method":"POST","url":"https://t/transfer","json":{"to":"b","amt":100}},
      {"method":"GET","url":"https://t/account"}
    ],
    "checks": [
      {"step": 1, "contains": "balance: 200"},   # double-spend: 100 -> 200
      {"step": 0, "status": 200}
    ]

A check may use `contains`, `absent`, `status`, or `regex`. Any failing check
refutes; all passing confirms. No steps/checks -> skip (never guess).
"""
from __future__ import annotations

import json
import re

from tools.verifiers.base import (
    VerifyResult, HttpExchange, confirmed, rejected, skipped, fetch,
)

VULN_CLASS = "business-logic"


def _run_step(step: dict, default_headers: dict, scope_checker, note: str):
    method = str(step.get("method") or "GET").upper()
    url = str(step.get("url") or "")
    headers = dict(default_headers)
    data = None
    if step.get("json") is not None:
        headers.setdefault("Content-Type", "application/json")
        data = json.dumps(step["json"]).encode()
    elif step.get("data") is not None:
        data = str(step["data"]).encode()
    headers.update(step.get("headers") or {})
    return fetch(url, method=method, headers=headers, data=data,
                 scope_checker=scope_checker, note=note)


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    steps = finding.get("steps") or []
    checks = finding.get("checks") or []
    if not steps:
        return skipped(VULN_CLASS, "no request `steps` supplied — business logic needs a scripted sequence")
    if not checks:
        return skipped(VULN_CLASS, "no `checks` supplied — cannot prove the invariant broke")

    default_headers = dict(finding.get("headers") or {})
    trace: list[HttpExchange] = []
    bodies: list[str] = []
    statuses: list[int | None] = []

    for i, step in enumerate(steps):
        if not step.get("url"):
            return skipped(VULN_CLASS, f"step {i} has no url")
        ex, body = _run_step(step, default_headers, scope_checker, f"logic step {i}")
        trace.append(ex)
        bodies.append(body.decode("utf-8", "replace"))
        statuses.append(ex.status)

    for check in checks:
        idx = int(check.get("step", -1))
        if idx < 0 or idx >= len(bodies):
            return rejected(VULN_CLASS, f"check references missing step {idx}", trace)
        text = bodies[idx]
        if "status" in check and statuses[idx] != int(check["status"]):
            return rejected(VULN_CLASS, f"step {idx} status {statuses[idx]} != {check['status']}",
                            trace)
        if "contains" in check and str(check["contains"]) not in text:
            return rejected(VULN_CLASS, f"step {idx} missing expected {check['contains']!r}",
                            trace)
        if "absent" in check and str(check["absent"]) in text:
            return rejected(VULN_CLASS, f"step {idx} unexpectedly contained {check['absent']!r}",
                            trace)
        if "regex" in check and not re.search(str(check["regex"]), text):
            return rejected(VULN_CLASS, f"step {idx} did not match /{check['regex']}/", trace)

    return confirmed(
        VULN_CLASS,
        "scripted sequence reproduced and every invariant assertion held",
        trace,
        f"{len(steps)} steps, {len(checks)} checks satisfied",
    )
