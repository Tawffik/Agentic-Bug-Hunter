#!/usr/bin/env python3
"""SSRF verifier — OOB callback OR in-band internal-data oracle.

Blind SSRF is proved by an out-of-band callback (delegated to `oob.py`). When the
target echoes internal data back in-band (e.g. a cloud metadata document, an
internal admin page, a local file banner), that is a stronger proof and needs no
collaborator. This verifier routes by available evidence:

  - if the finding carries `oob_payloads`/`oob_interactions` -> OOB oracle
  - else if it carries `ssrf_target` + `success_marker` -> in-band marker oracle
  - else skip (never guess)

The in-band oracle confirms only when the marker appears for the SSRF target and
NOT for a benign control URL, so a page that always contains the marker cannot
false-positive.
"""
from __future__ import annotations

from tools.verifiers.base import (
    VerifyResult, HttpExchange, confirmed, rejected, skipped, fetch, set_param, finding_url,
)

VULN_CLASS = "ssrf"


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    if finding.get("oob_payloads") or finding.get("oob_interactions"):
        # Lazy import avoids a package-init cycle (ssrf <-> oob both under verifiers).
        from tools.verifiers import oob as _oob
        return _oob.verify({**finding, "vuln_class": "ssrf"}, scope_checker=scope_checker)

    url = finding_url(finding)
    param = finding.get("param")
    target = finding.get("ssrf_target")
    marker = finding.get("success_marker")
    if not url or not param:
        return skipped(VULN_CLASS, "in-band SSRF needs url + param (or supply oob_* fields)")
    if not target:
        return skipped(VULN_CLASS, "no ssrf_target (internal URL) supplied")
    if not marker:
        return skipped(VULN_CLASS, "no success_marker to prove internal data was returned")

    trace: list[HttpExchange] = []
    ex_t, body_t = fetch(set_param(url, param, str(target)), scope_checker=scope_checker,
                         note="ssrf in-band internal target")
    trace.append(ex_t)
    hit = str(marker) in body_t.decode("utf-8", "replace")

    control = str(finding.get("control_target") or "https://example.com/")
    ex_c, body_c = fetch(set_param(url, param, control), scope_checker=scope_checker,
                         note="ssrf benign control")
    trace.append(ex_c)
    in_control = str(marker) in body_c.decode("utf-8", "replace")

    if hit and not in_control:
        return confirmed(
            VULN_CLASS,
            "internal target returned a marker absent from the benign control",
            trace,
            f"marker {marker!r} served only for {target!r}",
        )
    if in_control:
        return rejected(VULN_CLASS, "marker appears even for the benign control — not SSRF",
                        trace)
    return rejected(VULN_CLASS, "internal target did not return the marker", trace)
