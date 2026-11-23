#!/usr/bin/env python3
"""Web-cache-poisoning verifier — poison-then-clean oracle.

A header injection is only cache poisoning if the poisoned value is SERVED FROM
CACHE to a subsequent clean request. This verifier:

  1. poisons a unique cache-buster URL by sending `X-Forwarded-Host: <marker>`
  2. re-requests the SAME URL with NO injected header
  3. confirms ONLY when the marker is still served on the clean request

If the marker is absent on the clean request the cache did not store the poison
(a reflected-but-uncached header is not a finding).
"""
from __future__ import annotations

import secrets

from tools.verifiers.base import (
    VerifyResult, confirmed, rejected, skipped, fetch, set_param, finding_url,
)

VULN_CLASS = "cache-poisoning"


def verify(finding: dict, scope_checker=None) -> VerifyResult:
    url = finding_url(finding)
    if not url:
        return skipped(VULN_CLASS, "no url in finding")

    header = str(finding.get("inject_header") or "X-Forwarded-Host")
    marker = str(finding.get("marker_host") or f"poison-{secrets.token_hex(4)}.example")
    param = str(finding.get("cache_buster_param") or "cb")
    cb = secrets.token_hex(6)

    # Unique cache key so we never poison (or read) a real cached entry.
    target = set_param(url, param, cb)
    trace = []

    # 1) Poison the cache entry.
    poison_headers = dict(finding.get("headers") or {})
    poison_headers[header] = marker
    ex_p, body_p = fetch(target, headers=poison_headers, scope_checker=scope_checker,
                         note=f"cache-poison inject {header}")
    trace.append(ex_p)
    if ex_p.status is None:
        return rejected(VULN_CLASS, "poison request failed", trace, "no response")

    # 2) Clean request for the SAME key — no injected header.
    ex_c, body_c = fetch(target, headers=dict(finding.get("headers") or {}),
                         scope_checker=scope_checker, note="cache-poison clean request")
    trace.append(ex_c)
    text = body_c.decode("utf-8", "replace")

    if marker in text:
        return confirmed(
            VULN_CLASS,
            "poisoned header value was served from cache on a clean request",
            trace,
            f"{header}: {marker} persisted on cache key {param}={cb}",
        )
    if marker in body_p.decode("utf-8", "replace"):
        return rejected(VULN_CLASS,
                        "header reflected but not cached — no poisoning", trace)
    return rejected(VULN_CLASS, "marker not present after poisoning", trace)
