#!/usr/bin/env python3
"""Evidence contract — the four-part bar a finding must clear to be reportable.

Borrowed from ATOBench's finding that a "confirmed" result is meaningless unless
the *evidence chain* is grounded. A finding is reportable only when all four
parts hold:

    proof         a deterministic oracle fired (verifier confirmed) or a bundle exists
    ownership     the identity/tenant boundary is demonstrated (access-control classes)
    artifact      there is a reproducible request/response trace to attach
    report_support impact + severity are stated (advisory, not gating)

`assess()` is pure and side-effect free. `enforce()` is the opt-in hard gate used
by validate_core when a finding sets `strict_contract: true`. Everything degrades
safely: a missing part never silently passes — it is listed in `missing`.
"""
from __future__ import annotations

_ACCESS_CLASSES = {
    "idor", "graphql-idor", "auth-bypass", "mass-assignment",
    "business-logic", "privilege-escalation",
}

_IMPACT_KEYS = ("impact", "impact_statement", "pii_exfiltrated", "data_exfiltrated")


def _canon(finding: dict) -> str:
    raw = str(finding.get("vuln_class") or finding.get("vuln_type") or "")
    key = " ".join(raw.strip().lower().replace("_", " ").replace("-", " ").split())
    return key.replace(" ", "-")


def assess(finding: dict, verify_result=None) -> dict:
    """Assess the evidence contract for a finding + verifier result.

    `verify_result` is a `VerifyResult` (or None). Returns a dict with per-part
    booleans, an overall `satisfied`, and a human-readable `missing` list.
    """
    canon = _canon(finding)

    # proof ---------------------------------------------------------------
    proof = bool(verify_result is not None and getattr(verify_result, "confirmed", False))
    if not proof:
        proof = bool(finding.get("poc_bundle") or finding.get("verification_path"))

    # ownership -----------------------------------------------------------
    requires_ownership = canon in _ACCESS_CLASSES or bool(finding.get("requires_ownership"))
    if requires_ownership:
        identity = finding.get("attacker_headers") or finding.get("identity_a")
        victim = finding.get("victim_marker") or finding.get("success_marker")
        ownership = bool(identity and victim)
    else:
        ownership = True

    # artifact ------------------------------------------------------------
    has_trace = bool(verify_result is not None and getattr(verify_result, "trace", None))
    has_target = bool(finding.get("url") or finding.get("endpoint")
                      or finding.get("victim_object_url"))
    artifact = bool(has_trace or finding.get("poc_bundle") or has_target)

    # report support (advisory) ------------------------------------------
    has_impact = any(bool(finding.get(k)) for k in _IMPACT_KEYS)
    has_severity = bool(finding.get("severity") or finding.get("cvss")
                        or finding.get("cvss_vector"))
    report_support = bool(has_impact and has_severity)

    parts = {
        "proof": proof,
        "ownership": ownership,
        "artifact": artifact,
        "report_support": report_support,
    }
    missing = []
    if not proof:
        missing.append("proof: no deterministic oracle fired and no evidence bundle")
    if not ownership:
        missing.append("ownership: access-control class needs a second identity + victim marker")
    if not artifact:
        missing.append("artifact: no reproducible request/response trace")
    if not report_support:
        missing.append("report_support: impact and severity not stated")

    return {
        "schema": "evidence-contract/1",
        "vuln_class": canon,
        "requires_ownership": requires_ownership,
        "parts": parts,
        # report_support is advisory; the three hard parts gate reportability.
        "satisfied": proof and ownership and artifact,
        "missing": missing,
    }


def enforce(finding: dict, verify_result=None) -> tuple[bool, dict]:
    """Return (satisfied, contract). Never raises; safe to call anywhere."""
    contract = assess(finding, verify_result)
    return bool(contract["satisfied"]), contract
