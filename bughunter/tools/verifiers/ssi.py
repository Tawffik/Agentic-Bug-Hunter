#!/usr/bin/env python3
"""SSI (Server-Side Includes) injection verifier — command-output canary oracle.

SSI injection is confirmed only when the server *executes* the directive and its
command output is returned. A page that reflects `<!--#exec ...-->` verbatim is
NOT vulnerable (that is the classic false positive). The oracle therefore
requires the evaluated canary to appear while the literal directive does not.

Payload:  <!--#exec cmd="printf SSI<rand>"-->
Confirm:  body contains SSI<rand> AND the literal directive is absent
Reject:   literal directive echoed unprocessed (no SSI) OR canary absent
"""
from __future__ import annotations

import secrets

from tools.verifiers.base import (
    VerifyResult, confirmed, rejected, skipped, fetch, set_param, finding_url,
)

VULN_CLASS = "ssi"


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    url = finding_url(finding)
    param = finding.get("param")
    if not url or not param:
        return skipped(VULN_CLASS, "ssi verifier needs both url and param")

    canary = "SSI" + secrets.token_hex(6)
    literal = f'<!--#exec cmd="printf {canary}"-->'

    ex_b, body_b = fetch(set_param(url, param, "1"), scope_checker=scope_checker,
                         note="ssi baseline")
    ex_p, body_p = fetch(set_param(url, param, literal), scope_checker=scope_checker,
                         note="ssi probe")
    text = body_p.decode("utf-8", "replace")
    base = body_b.decode("utf-8", "replace")

    if canary in text and literal not in text and canary not in base:
        return confirmed(
            VULN_CLASS,
            "SSI directive executed (canary output present, directive not reflected)",
            [ex_b, ex_p],
            f"canary {canary} rendered by <!--#exec-->",
        )
    if literal in text:
        return rejected(VULN_CLASS, "directive reflected unprocessed (no SSI)", [ex_b, ex_p])
    return rejected(VULN_CLASS, "no SSI output", [ex_b, ex_p])