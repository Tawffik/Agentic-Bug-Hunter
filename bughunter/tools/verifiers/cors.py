#!/usr/bin/env python3
"""CORS misconfiguration verifier — credentialed-reflection oracle.

A reflective `Access-Control-Allow-Origin` is noise unless the response ALSO
grants credentials (`Access-Control-Allow-Credentials: true`). Only then can a
malicious origin read authenticated user data. This verifier sends an attacker
Origin and confirms ONLY on the exact combination:

    ACAO == attacker origin (not a wildcard)  AND  ACAC == "true"

Wildcard `*` + credentials is browser-invalid, so it is not confirmed. A
reflection without credentials is rejected (informational, not a data-exfil
break) — matching the triage never-submit rule.
"""
from __future__ import annotations

from tools.verifiers.base import (
    VerifyResult, confirmed, rejected, skipped, fetch, finding_url,
)

VULN_CLASS = "cors"


def _h(headers: dict, name: str) -> str:
    for k, v in (headers or {}).items():
        if k.lower() == name.lower():
            return str(v)
    return ""


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    url = finding_url(finding)
    if not url:
        return skipped(VULN_CLASS, "no url in finding")

    attacker = str(finding.get("attacker_origin") or "https://attacker.example").rstrip("/")
    headers = dict(finding.get("headers") or {})
    headers["Origin"] = attacker

    ex, _ = fetch(url, headers=headers, scope_checker=scope_checker,
                  note="cors credentialed-reflection probe")
    trace = [ex]

    if ex.status is None:
        return rejected(VULN_CLASS, "request failed", trace, "no response")
    if ex.status >= 400:
        return rejected(VULN_CLASS, "endpoint did not accept the request", trace,
                        f"status {ex.status}")

    acao = _h(ex.response_headers, "Access-Control-Allow-Origin")
    acac = _h(ex.response_headers, "Access-Control-Allow-Credentials")
    if not acao:
        return rejected(VULN_CLASS, "no Access-Control-Allow-Origin header", trace)

    if acac.strip().lower() != "true":
        return rejected(VULN_CLASS,
                        "origin reflected but credentials not allowed — no authenticated read",
                        trace, f"ACAO={acao!r} ACAC={acac!r}")

    if acao.strip() == "*":
        return rejected(VULN_CLASS,
                        "wildcard with credentials is browser-invalid — not exploitable",
                        trace, "ACAO=* ACAC=true")

    if acao.strip().rstrip("/") != attacker:
        return rejected(VULN_CLASS, "ACAO does not reflect the attacker origin", trace,
                        f"ACAO={acao!r}, expected {attacker!r}")

    return confirmed(
        VULN_CLASS,
        "attacker origin reflected with Access-Control-Allow-Credentials: true",
        trace,
        f"ACAO={attacker!r} + ACAC=true — credentialed cross-origin read",
    )
