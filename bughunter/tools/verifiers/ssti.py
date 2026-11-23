#!/usr/bin/env python3
"""SSTI verifier — server-side arithmetic-evaluation oracle.

Reflection is not template injection. This verifier injects an arithmetic
expression wrapped in common template syntaxes and confirms ONLY when the
server-evaluated product appears while the raw payload does not. Using two
4-digit operands makes an accidental page match effectively impossible.

Example: `{{7393*911}}` -> `6735023`. If the response contains `6735023` but not
the literal `{{7393*911}}`, the template engine evaluated our expression.
"""
from __future__ import annotations

from tools.verifiers.base import (
    VerifyResult, confirmed, rejected, skipped, fetch, set_param, finding_url,
)

VULN_CLASS = "ssti"

_LEFT = 7393
_RIGHT = 911
_PRODUCT = _LEFT * _RIGHT  # 6735023

# Ordered by likelihood; the finding may pin one via "engine".
_PAYLOADS = [
    ("jinja/twig", "{{%d*%d}}" % (_LEFT, _RIGHT)),
    ("freemarker", "${{%d*%d}}" % (_LEFT, _RIGHT)),
    ("erb/ejs", "<%%= %d*%d %%>" % (_LEFT, _RIGHT)),
    ("ruby", "#{%d*%d}" % (_LEFT, _RIGHT)),
    ("velocity", "$!{%d*%d}" % (_LEFT, _RIGHT)),
    ("generic", "${%d*%d}" % (_LEFT, _RIGHT)),
]


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    url = finding_url(finding)
    param = finding.get("param")
    if not url or not param:
        return skipped(VULN_CLASS, "ssti verifier needs both url and param")

    engine = str(finding.get("engine") or "").lower()
    payloads = [p for p in _PAYLOADS if not engine or engine in p[0]] or _PAYLOADS

    trace = []
    raw_seen = False
    for name, payload in payloads:
        ex, body = fetch(set_param(url, param, payload), scope_checker=scope_checker,
                         note=f"ssti {name} probe")
        trace.append(ex)
        text = body.decode("utf-8", "replace")
        if payload in text:
            raw_seen = True
        if str(_PRODUCT) in text and payload not in text:
            return confirmed(
                VULN_CLASS,
                "server evaluated the injected arithmetic expression",
                trace,
                f"{payload!r} rendered {_PRODUCT} (engine hint: {name})",
            )

    if raw_seen:
        return rejected(VULN_CLASS, "payload reflected literally — no evaluation", trace)
    return rejected(VULN_CLASS, "evaluated result never appeared", trace)
