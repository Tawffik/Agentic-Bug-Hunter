#!/usr/bin/env python3
"""GraphQL IDOR/BOLA verifier — two-identity query differential oracle.

GraphQL hides object access behind arbitrary query shapes, so a REST-style IDOR
verifier cannot see it. This verifier replays the SAME operation with two
identities and confirms cross-tenant read only when:

  - the attacker identity's query returns the victim's unique marker, AND
  - an anonymous query for the same object does NOT return it (so a public
    object cannot masquerade as an access-control break).

Without a second identity + a victim marker it skips (GraphQL IDOR is
notoriously easy to fake with your own data).
"""
from __future__ import annotations

import json

from tools.verifiers.base import (
    VerifyResult, HttpExchange, confirmed, rejected, skipped, fetch, finding_url,
)

VULN_CLASS = "graphql-idor"


def _query(finding: dict) -> str:
    q = finding.get("query")
    if q:
        return str(q)
    obj = str(finding.get("object") or "user")
    return ("query ($id: ID!) { %s(id: $id) { id email name } }" % obj)


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    url = finding_url(finding)
    attacker_headers = finding.get("attacker_headers") or finding.get("identity_a")
    victim_marker = finding.get("victim_marker")
    if not url:
        return skipped(VULN_CLASS, "no graphql url in finding")
    if not attacker_headers:
        return skipped(VULN_CLASS, "no attacker identity (attacker_headers)")
    if not victim_marker:
        return skipped(VULN_CLASS, "no victim_marker to prove cross-tenant read")

    payload = json.dumps({
        "query": _query(finding),
        "variables": {"id": str(finding.get("victim_id") or finding.get("object_id") or "")},
    }).encode()

    a_headers = dict(attacker_headers)
    a_headers.setdefault("Content-Type", "application/json")
    trace: list[HttpExchange] = []

    ex_a, body_a = fetch(url, method="POST", headers=a_headers, data=payload,
                         scope_checker=scope_checker, note="gql attacker queries victim id")
    trace.append(ex_a)
    text_a = body_a.decode("utf-8", "replace")
    if ex_a.status != 200 or str(victim_marker) not in text_a:
        return rejected(VULN_CLASS, "attacker query did not return the victim marker", trace,
                        f"status {ex_a.status}, marker present={str(victim_marker) in text_a}")

    anon_headers = {"Content-Type": "application/json"}
    ex_n, body_n = fetch(url, method="POST", headers=anon_headers, data=payload,
                         scope_checker=scope_checker, note="gql anon control")
    trace.append(ex_n)
    if ex_n.status == 200 and str(victim_marker) in body_n.decode("utf-8", "replace"):
        return rejected(VULN_CLASS,
                        "object is public (anonymous query also returned it)", trace)

    return confirmed(
        VULN_CLASS,
        "attacker query returned another tenant's object; anonymous query denied",
        trace,
        f"victim marker {victim_marker!r} returned to attacker identity",
    )
