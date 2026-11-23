#!/usr/bin/env python3
"""Mass-assignment verifier — privileged-field persistence oracle.

The bug is not "the server ignored my field"; it is "the server accepted a field
the user should not control and it now affects state." This verifier proves that
deterministically:

  1. baseline: send the body WITHOUT the privileged field -> marker absent
  2. injection: send the body WITH `field=<unique marker>`
  3. confirm ONLY if the marker is observable afterwards (in the inject response
     or a read-back GET) AND was absent in the baseline.

Without a unique marker + read-back we skip — a reflected field is not proof it
was persisted.
"""
from __future__ import annotations

import json

from tools.verifiers.base import (
    VerifyResult, HttpExchange, confirmed, rejected, skipped, fetch, finding_url,
)

VULN_CLASS = "mass-assignment"


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    url = finding_url(finding)
    field = finding.get("field")
    if not url:
        return skipped(VULN_CLASS, "no url in finding")
    if not field:
        return skipped(VULN_CLASS, "no privileged `field` to inject")

    marker = str(finding.get("value") or finding.get("marker") or "")
    if not marker:
        return skipped(VULN_CLASS, "no unique `value`/`marker` — cannot prove persistence")

    method = str(finding.get("method") or "POST").upper()
    headers = dict(finding.get("headers") or {})
    headers.setdefault("Content-Type", "application/json")
    base_body = dict(finding.get("body") or {})

    trace: list[HttpExchange] = []

    # 1) Baseline without the privileged field.
    ex_b, body_b = fetch(url, method=method, headers=headers,
                         data=json.dumps(base_body).encode(), scope_checker=scope_checker,
                         note="mass-assignment baseline (field omitted)")
    trace.append(ex_b)
    if marker in body_b.decode("utf-8", "replace"):
        return rejected(VULN_CLASS, "marker present without injection — not injectable",
                        trace, "baseline already contained the marker")

    # 2) Inject the privileged field.
    injected = dict(base_body)
    injected[field] = marker
    ex_i, body_i = fetch(url, method=method, headers=headers,
                         data=json.dumps(injected).encode(), scope_checker=scope_checker,
                         note=f"mass-assignment inject {field}")
    trace.append(ex_i)
    if ex_i.status is None:
        return rejected(VULN_CLASS, "injection request failed", trace, "no response")

    inject_text = body_i.decode("utf-8", "replace")
    if marker in inject_text:
        return confirmed(VULN_CLASS, "privileged field accepted and echoed", trace,
                         f"field {field!r}={marker!r} survived into the response")

    # 3) Read-back to prove persistence (stronger than an echo).
    readback = str(finding.get("readback_url") or "")
    if readback:
        rb_headers = dict(finding.get("readback_headers") or headers)
        ex_r, body_r = fetch(readback, headers=rb_headers, scope_checker=scope_checker,
                            note="mass-assignment read-back")
        trace.append(ex_r)
        if marker in body_r.decode("utf-8", "replace"):
            return confirmed(VULN_CLASS, "privileged field persisted (survived read-back)",
                             trace, f"field {field!r}={marker!r} read back from state")

    return rejected(VULN_CLASS, "privileged field was not observable after injection", trace)
