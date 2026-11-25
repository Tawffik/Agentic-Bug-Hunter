"""Eval harness — report-gate fixtures (rubric dimension: gate correctness, weight 30%).

Implements fixtures F1/F2 (+ two boundary cases) from
coordination/agent-eval-rubric.md against the deterministic report gate in
bughunter/brain.py. Runs fully offline: no provider calls, no network.
This measures the deterministic gate logic only — it does NOT measure model
quality; a real baseline needs a verified free provider (see agent-run-pilot.md).

Each fixture writes synthetic validation.json files into a temp findings dir
and asserts the gate's accept/reject decision. Results print as one JSON line
per fixture (EVAL_RESULT {...}) for the future baseline-vs-candidate runner.
"""

import json
import os
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for path in (os.path.join(REPO_ROOT, "bughunter"), os.path.join(REPO_ROOT, "bughunter", "tools")):
    if path not in sys.path:
        sys.path.insert(0, path)

import brain  # noqa: E402


def _bare_brain():
    b = brain.Brain.__new__(brain.Brain)
    b.enabled = True
    b.model = "eval-offline"
    return b


def _write_validation(finding_dir, payload):
    finding_dir.mkdir(parents=True, exist_ok=True)
    (finding_dir / "validation.json").write_text(json.dumps(payload), encoding="utf-8")


def _emit(fixture, expected_ready, actual_ready, note):
    record = {
        "fixture": fixture,
        "expected_ready": expected_ready,
        "actual_ready": actual_ready,
        "pass": expected_ready == actual_ready,
        "note": note[:120],
    }
    print("EVAL_RESULT " + json.dumps(record, ensure_ascii=False))
    return record


def test_f1_strong_validated_finding_is_accepted(tmp_path):
    """F1: a finding with status=validated_finding and a confirmed verifier
    trace must pass the gate (no false rejection)."""
    _write_validation(tmp_path / "xss-reflected", {
        "status": "validated_finding",
        "verifier": {"confirmed": True, "tool": "synthetic-fixture"},
        "adversarial": {"verdict": "SUSTAINED"},
    })
    ready, note = _bare_brain()._report_gate(str(tmp_path))
    rec = _emit("F1-strong-finding", True, ready, note)
    assert rec["pass"], note


def test_f2_weak_theoretical_finding_is_rejected(tmp_path):
    """F2: an unvalidated finding (status=unconfirmed) must be blocked
    (no false acceptance)."""
    _write_validation(tmp_path / "xss-theoretical", {
        "status": "unconfirmed",
        "rejection_reasons": ["no reproduction steps"],
        "verifier": {"confirmed": False},
    })
    ready, note = _bare_brain()._report_gate(str(tmp_path))
    rec = _emit("F2-weak-finding", False, ready, note)
    assert rec["pass"]
    assert "NO_REPORTS" in note


def test_no_validation_files_blocks_by_default(tmp_path):
    """Boundary: empty findings dir -> blocked unless the explicit legacy
    override env var is set."""
    ready, note = _bare_brain()._report_gate(str(tmp_path))
    rec = _emit("B1-no-validations", False, ready, note)
    assert rec["pass"]
    assert "NO_REPORTS" in note


def test_override_env_allows_manual_review_path(tmp_path, monkeypatch):
    """Boundary: BBHUNT_ALLOW_UNVALIDATED_REPORT=1 opens the legacy path
    (documents the bypass so the baseline records when it is used)."""
    monkeypatch.setenv("BBHUNT_ALLOW_UNVALIDATED_REPORT", "1")
    ready, note = _bare_brain()._report_gate(str(tmp_path))
    rec = _emit("B2-env-override", True, ready, note)
    assert rec["pass"]
