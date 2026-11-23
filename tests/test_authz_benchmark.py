#!/usr/bin/env python3
"""CI smoke test for the authz differential benchmark."""
from __future__ import annotations

from tests.benchmark import authz_score


def test_authz_differential_benchmark_passes():
    report = authz_score.run()
    assert report["recall"] == 1.0, report["results"]
    assert report["confirmed_fp"] == 0, report["results"]
    assert report["marker_lead_fp"] == 0, report["results"]
    assert report["verdict_accuracy"] == 1.0, report["results"]
