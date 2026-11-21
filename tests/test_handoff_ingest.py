"""Lifecycle handoff validation/ingest tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import handoff_ingest as hi  # noqa: E402


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
