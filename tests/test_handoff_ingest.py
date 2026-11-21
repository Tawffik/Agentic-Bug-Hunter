"""Lifecycle handoff validation/ingest tests."""
from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import handoff_ingest as hi  # noqa: E402
import lead_board as lb  # noqa: E402


@pytest.fixture
def board(tmp_path, monkeypatch):
    monkeypatch.setattr(lb, "LEADS_DIR", str(tmp_path / "leads"))
    return tmp_path


def _leads(tmp_path, status: str = "new") -> Path:
    return _write_handoff(tmp_path, [
        {"id": "l1", "class": "idor", "severity": "high", "confidence": "medium",
         "status": status, "source": "hunter", "dedupe_key": "a", "evidence_ref": "r1"},
        {"id": "l2", "class": "xss", "severity": "critical", "confidence": "high",
         "status": "new", "source": "hunter", "dedupe_key": "b", "evidence_ref": "r2"},
    ])


def _run(d, state, *extra) -> dict:
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = hi.main([str(d), "--state", str(state), "--json", *extra])
    out = json.loads(buf.getvalue())
    out["rc"] = rc
    return out


def _write_handoff(tmp_path: Path, leads: list[dict]) -> Path:
    d = tmp_path / "handoff"
    d.mkdir()
    (d / "target_profile.json").write_text(json.dumps({
        "target": "example.com", "scope": ["*.example.com"], "platform": "hackerone",
        "program": "example", "technologies": [{"vendor": "nginx", "product": "nginx"}],
    }))
    (d / "assets.jsonl").write_text(json.dumps({"host": "example.com", "source": "live",
                                                "scope_status": "in_scope"}) + "\n")
    (d / "leads.jsonl").write_text("\n".join(json.dumps(x) for x in leads) + "\n")
    (d / "evidence.json").write_text(json.dumps([{"id": "e1", "type": "request", "ref": "run.log"}]))
    (d / "run_meta.json").write_text(json.dumps({
        "run_id": "123", "target": "example.com", "producer": "BugBountyCI",
        "generated_at": "2026-11-21T00:00:00Z",
    }))
    return d


def test_validate_and_rank(tmp_path):
    d = _write_handoff(tmp_path, [
        {"id": "l1", "class": "idor", "severity": "high", "confidence": "medium",
         "status": "new", "source": "hunter", "dedupe_key": "a"},
        {"id": "l2", "class": "xss", "severity": "critical", "confidence": "high",
         "status": "new", "source": "hunter", "dedupe_key": "b"},
        {"id": "l3", "class": "idor", "severity": "high", "confidence": "medium",
         "status": "new", "source": "hunter", "dedupe_key": "a"},
    ])
    handoff = hi.load_handoff(d)
    leads = hi.normalize_leads(handoff["leads"])
    assert len(leads) == 2
    assert leads[0].id == "l2"


def test_missing_required_field_fails(tmp_path):
    d = _write_handoff(tmp_path, [])
    (d / "run_meta.json").write_text(json.dumps({"run_id": "1"}))
    proc = subprocess.run([sys.executable, str(TOOLS / "handoff_ingest.py"), str(d)],
                          capture_output=True, text=True)
    assert proc.returncode == 1
    assert "invalid handoff" in proc.stderr


def test_empty_technologies_is_valid(tmp_path):
    d = _write_handoff(tmp_path, [])
    import json
    profile = json.loads((d / "target_profile.json").read_text())
    profile["technologies"] = []
    (d / "target_profile.json").write_text(json.dumps(profile))
    handoff = hi.load_handoff(d)
    assert handoff["target_profile"]["technologies"] == []


def test_preview_does_not_write_state(tmp_path, board):
    d = _leads(tmp_path)
    state = tmp_path / "state.json"
    out = _run(d, state)
    assert out["new_leads"] == 2
    assert out["ingested"] is None or "ingested" not in out
    assert not state.exists()


def test_ingest_is_delta_first(tmp_path, board):
    d = _leads(tmp_path)
    state = tmp_path / "state.json"
    first = _run(d, state, "--ingest")
    assert first["rc"] == 0 and first["ingested"] == 2
    second = _run(d, state, "--ingest")
    assert second["rc"] == 0
    assert second["new_leads"] == 0 and second["ingested"] == 0
    assert second["skipped_seen"] == 2 and second["already_ingested_run"] is True
    assert len(lb.load_ledger("example.com")) == 2


def test_changed_status_reconciles_without_duplicate(tmp_path, board):
    d = _leads(tmp_path)
    state = tmp_path / "state.json"
    _run(d, state, "--ingest")
    (d / "leads.jsonl").write_text("\n".join(json.dumps(x) for x in [
        {"id": "l1", "class": "idor", "severity": "high", "confidence": "medium",
         "status": "killed", "source": "hunter", "dedupe_key": "a", "evidence_ref": "r1"},
        {"id": "l2", "class": "xss", "severity": "critical", "confidence": "high",
         "status": "new", "source": "hunter", "dedupe_key": "b", "evidence_ref": "r2"},
    ]))
    (d / "run_meta.json").write_text(json.dumps({
        "run_id": "124", "target": "example.com", "producer": "BugBountyCI",
        "generated_at": "2026-11-21T01:00:00Z",
    }))
    out = _run(d, state, "--ingest")
    assert out["rc"] == 0
    assert out["ingested"] == 0 and out["updated"] == 1
    rows = lb.load_ledger("example.com")
    assert len(rows) == 2
    assert next(l for l in rows if l["finding_id"] == "l1")["status"] == "killed"


def test_reset_delta_reingests_without_board_duplicates(tmp_path, board):
    d = _leads(tmp_path)
    state = tmp_path / "state.json"
    _run(d, state, "--ingest")
    out = _run(d, state, "--ingest", "--reset-delta")
    assert out["new_leads"] == 2 and out["ingested"] == 2
    assert len(lb.load_ledger("example.com")) == 2


def test_state_file_is_owner_only(tmp_path, board):
    d = _leads(tmp_path)
    state = tmp_path / "mem" / "state.json"
    _run(d, state, "--ingest")
    assert stat.S_IMODE(os.stat(state).st_mode) == 0o600
