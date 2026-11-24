#!/usr/bin/env python3
"""Deterministic verifier library — the false-positive killer.

Discovery and verification are separate systems: an agent/scanner that surfaces
a candidate finding can never confirm its own bug. A finding stays a *lead*
until the matching verifier here reproduces it against the live target and a
deterministic (non-AI) oracle fires. Verifiers return a boolean + a reproducible
trace, never a confidence score.

Public API:
    verify_finding(finding, scope_checker=None) -> VerifyResult
    REGISTRY: dict[str, callable]   # canonical vuln_class -> verify fn
    normalize_class(name) -> str    # alias -> canonical class
"""
from __future__ import annotations

from tools.verifiers.base import VerifyResult, skipped
from tools.verifiers import (
    redirect, sensitive_file, auth_bypass, sqli, idor, oob, xss,
    cors, mass_assignment, ssti, graphql_idor, ssrf, llm_exfil,
    business_logic, cache_poison, ssi, web3_poc,
)

# canonical class -> verify callable
REGISTRY = {
    "open-redirect": redirect.verify,
    "sensitive-file": sensitive_file.verify,
    "auth-bypass": auth_bypass.verify,
    "sqli": sqli.verify,
    "idor": idor.verify,
    "xss": xss.verify,
    "ssrf": ssrf.verify,          # OOB or in-band, routed by available evidence
    "xxe": oob.verify,
    "rce": oob.verify,
    "log4shell": oob.verify,
    "cors": cors.verify,
    "mass-assignment": mass_assignment.verify,
    "ssti": ssti.verify,
    "graphql-idor": graphql_idor.verify,
    "llm-exfil": llm_exfil.verify,
    "business-logic": business_logic.verify,
    "cache-poisoning": cache_poison.verify,
    "ssi": ssi.verify,
    "web3-poc": web3_poc.verify,
}

# alias -> canonical class (lowercased, punctuation-insensitive match applied)
_ALIASES = {
    "open redirect": "open-redirect",
    "openredirect": "open-redirect",
    "redirect": "open-redirect",
    "sensitive file": "sensitive-file",
    "sensitive file exposure": "sensitive-file",
    "info disclosure": "sensitive-file",
    "information disclosure": "sensitive-file",
    "exposure": "sensitive-file",
    "source-leak": "sensitive-file",
    "source leak": "sensitive-file",
    "auth bypass": "auth-bypass",
    "authentication bypass": "auth-bypass",
    "broken access control": "auth-bypass",
    "broken access": "auth-bypass",
    "bac": "auth-bypass",
    "forced browsing": "auth-bypass",
    "sql injection": "sqli",
    "sql-injection": "sqli",
    "blind sqli": "sqli",
    "bola": "idor",
    "insecure direct object reference": "idor",
    "broken object level authorization": "idor",
    "reflected xss": "xss",
    "stored xss": "xss",
    "dom xss": "xss",
    "cross-site scripting": "xss",
    "cross site scripting": "xss",
    "server-side request forgery": "ssrf",
    "server side request forgery": "ssrf",
    "xml external entity": "xxe",
    "command injection": "rce",
    "os command injection": "rce",
    "remote code execution": "rce",
    "log4j": "log4shell",
    # 2026 additions
    "cors misconfiguration": "cors",
    "cross-origin resource sharing": "cors",
    "mass assignment": "mass-assignment",
    "parameter pollution / over-posting": "mass-assignment",
    "over-posting": "mass-assignment",
    "autobinding": "mass-assignment",
    "server-side template injection": "ssti",
    "template injection": "ssti",
    "graphql idor": "graphql-idor",
    "graphql bola": "graphql-idor",
    "graphql broken object level authorization": "graphql-idor",
    "graphql object access": "graphql-idor",
    "llm exfiltration": "llm-exfil",
    "prompt exfiltration": "llm-exfil",
    "system prompt leak": "llm-exfil",
    "canary exfiltration": "llm-exfil",
    # routing label hunt-llm-ai -> llm-exfil (canary oracle; skips without marker)
    "llm ai": "llm-exfil",
    "llm": "llm-exfil",
    # SAML ACS is an XML parser -> the OOB/XXE oracle (skips without payloads)
    "saml": "xxe",
    "saml acs": "xxe",
    "business logic": "business-logic",
    "business-logic error": "business-logic",
    "logic flaw": "business-logic",
    "cache poisoning": "cache-poisoning",
    "web cache poisoning": "cache-poisoning",
    "cache deception": "cache-poisoning",
    "ssi injection": "ssi",
    "server-side includes": "ssi",
    "server side include": "ssi",
    "server-side include injection": "ssi",
    "web3 poc": "web3-poc",
    "web3-poc": "web3-poc",
    "smart contract poc": "web3-poc",
    "missing access control": "web3-poc",
    "reentrancy": "web3-poc",
}


def normalize_class(name: str) -> str:
    """Map a free-form vuln name onto a canonical verifier class ('' if none)."""
    if not name:
        return ""
    key = " ".join(str(name).strip().lower().replace("_", " ").replace("-", " ").split())
    # direct canonical (with hyphens) check first
    canon_hyphen = key.replace(" ", "-")
    if canon_hyphen in REGISTRY:
        return canon_hyphen
    if key in REGISTRY:
        return key
    if key in _ALIASES:
        return _ALIASES[key]
    # substring fallback for noisy scanner labels ("reflected xss in q param")
    for alias, canon in _ALIASES.items():
        if alias in key:
            return canon
    for canon in REGISTRY:
        if canon.replace("-", " ") in key:
            return canon
    return ""


def verify_finding(finding: dict, scope_checker=None) -> VerifyResult:
    """Dispatch a finding to its deterministic verifier.

    `finding` carries at least a vuln_class/vuln_type plus the fields that
    verifier needs (url, param, markers, identities, oob_* ...). An unknown
    class is skipped — never silently passed.
    """
    raw = finding.get("vuln_class") or finding.get("vuln_type") or ""
    canon = normalize_class(raw)
    if not canon:
        return skipped(str(raw) or "unknown", f"no verifier registered for class {raw!r}")
    fn = REGISTRY[canon]
    # oob.verify reads vuln_class off the finding; make sure it is canonical.
    enriched = dict(finding)
    enriched.setdefault("vuln_class", canon)
    if canon in ("ssrf", "xxe", "rce", "log4shell"):
        enriched["vuln_class"] = canon
    return fn(enriched, scope_checker=scope_checker)


__all__ = ["verify_finding", "REGISTRY", "normalize_class", "VerifyResult"]
