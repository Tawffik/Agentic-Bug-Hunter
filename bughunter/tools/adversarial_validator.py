#!/usr/bin/env python3
"""Adversarial validator — the finder's job is to prove, this job is to DISPROVE.

A confirmation oracle can still be fooled by a generic marker, a public resource,
or a page that echoes everything. This validator attacks the finding from the
opposite side and returns one of:

    SURVIVES       independent checks failed to break the finding
    FALSIFIED      a check showed the finding is not what it claims (kill it)
    INCONCLUSIVE   could not run the checks (network/teardown) — hold, don't ship

Design: `falsify()` is pure control flow over an injectable `fetcher`, so it is
unit-testable offline; only the default fetcher touches the network. It is the
adversarial counterpart to `verifiers/` — call it after a verifier confirms and
before a report is written (validate_core does this when `adversarial: true`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from tools.verifiers.base import fetch as _default_fetch, finding_url

_LOGIN_SIGNALS = ("login", "sign in", "sign-in", "please log in", "unauthorized",
                  "forbidden", "access denied", "not authorized")


def _marker(finding: dict) -> str:
    for key in ("victim_marker", "success_marker", "marker", "secret_marker",
                "canary", "value"):
        if finding.get(key):
            return str(finding[key])
    return ""


def _fetcher(fetcher, scope_checker):
    if fetcher is not None:
        return fetcher

    def _f(url, headers=None, method="GET", data=None):
        ex, body = _default_fetch(url, method=method, headers=headers, data=data,
                                  scope_checker=scope_checker, note="adversarial check")
        return ex.status, body.decode("utf-8", "replace")

    return _f


def falsify(finding: dict, scope_checker=None, fetcher=None) -> dict:
    """Try to disprove `finding`. Returns {"verdict", "reasons", "checks_run"}."""
    marker = _marker(finding)
    if not marker:
        return {"verdict": "INCONCLUSIVE", "reasons": ["no marker to falsify against"],
                "checks_run": 0}

    get = _fetcher(fetcher, scope_checker)
    reasons: list[str] = []
    ran = 0
    failed_network = 0

    def _safe(url, **kw):
        nonlocal ran, failed_network
        ran += 1
        try:
            return get(url, **kw)
        except Exception as exc:  # noqa: BLE001 - network failure is INCONCLUSIVE
            failed_network += 1
            reasons.append(f"check error on {url}: {type(exc).__name__}")
            return None, ""

    # 1) Public-resource check: the marker must NOT be readable anonymously.
    target = str(finding.get("victim_object_url") or finding_url(finding) or "")
    if target:
        status, text = _safe(target)
        if status is not None and marker in text and status == 200:
            low = text.lower()
            if (str(finding.get("vuln_class")) in ("auth-bypass", "forced-browse")
                    and any(sig in low for sig in _LOGIN_SIGNALS)):
                reasons.append("response looks like a login/denied page — not a bypass")
                return {"verdict": "FALSIFIED", "reasons": reasons, "checks_run": ran}
            reasons.append("marker is readable anonymously — resource is public, not a boundary break")
            return {"verdict": "FALSIFIED", "reasons": reasons, "checks_run": ran}

    # 2) Static/baseline check: the marker must NOT already be on a benign page.
    baseline = str(finding.get("baseline_url") or finding.get("control_url") or "")
    if baseline:
        status, text = _safe(baseline)
        if status is not None and marker in text:
            reasons.append("marker already present on the benign baseline — generic, not a bug")
            return {"verdict": "FALSIFIED", "reasons": reasons, "checks_run": ran}

    # 3) Own-object check (IDOR): the victim marker must not appear in the
    #    attacker's OWN object, or it was never another tenant's data.
    own = str(finding.get("attacker_object_url") or "")
    if own:
        headers = finding.get("attacker_headers") or finding.get("identity_a")
        status, text = _safe(own, headers=headers)
        if status is not None and marker in text:
            reasons.append("victim marker also appears in the attacker's own object — "
                           "not cross-tenant")
            return {"verdict": "FALSIFIED", "reasons": reasons, "checks_run": ran}

    # 4) Login/denied heuristic for any remaining auth-class finding.
    if target and finding.get("vuln_class") in ("auth-bypass", "forced-browse"):
        status, text = _safe(target)
        low = text.lower()
        if any(sig in low for sig in _LOGIN_SIGNALS):
            reasons.append("response looks like a login/denied page — not a bypass")
            return {"verdict": "FALSIFIED", "reasons": reasons, "checks_run": ran}

    if failed_network and ran == failed_network:
        return {"verdict": "INCONCLUSIVE", "reasons": reasons, "checks_run": ran}
    if not ran:
        return {"verdict": "INCONCLUSIVE",
                "reasons": ["no adversarial checks were applicable"], "checks_run": 0}
    return {"verdict": "SURVIVES",
            "reasons": reasons or ["no control request reproduced the marker"],
            "checks_run": ran}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Adversarially validate (try to falsify) a finding")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--finding", help="path to a finding JSON file")
    src.add_argument("--stdin", action="store_true", help="read finding JSON from stdin")
    args = ap.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.stdin else open(args.finding, encoding="utf-8").read()
        finding = json.loads(raw)
    except (OSError, ValueError) as exc:
        print(f"[-] bad finding input: {exc}", file=sys.stderr)
        return 3

    result = falsify(finding)
    print(json.dumps(result, indent=2))
    return 0 if result["verdict"] == "SURVIVES" else (1 if result["verdict"] == "FALSIFIED" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
