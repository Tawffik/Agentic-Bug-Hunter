"""Tests for the self-audit / continuous-evolution engine."""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import self_audit as sa  # noqa: E402


def _fake_repo(tmp_path: Path) -> Path:
    for name in ("skills/alpha", "skills/beta"):
        (tmp_path / name).mkdir(parents=True)
        (tmp_path / name / "SKILL.md").write_text("x")
    (tmp_path / "commands").mkdir()
    (tmp_path / "commands" / "hunt.md").write_text("x")
    (tmp_path / "bughunter" / "agents").mkdir(parents=True)
    (tmp_path / "bughunter" / "agents" / "recon.md").write_text("x")
    tools = tmp_path / "bughunter" / "tools"
    tools.mkdir()
    main_guard = "if __name__ == '__main__':\n    pass\n"
    for f in ("foo.py", "bar.py", "_private.py"):
        (tools / f).write_text(main_guard)
    (tools / "scan.sh").write_text("echo hi\n")
    (tools / "README.md").write_text("| Tool | Purpose |\n| `foo.py` | x |\n| `scan.sh` | x |\n| `external_arsenal.sh` | x |\n")
    (tools / "external_arsenal.sh").write_text(
        'ARSENAL_TOOLS=(\n'
        '  "nmap|recon|brew install nmap|x"\n'
        '  "ffuf|fuzz|go install|x"\n'
        ')\n'
    )
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text("x")
    return tmp_path


def test_parse_arsenal_from_real_repo():
    entries = sa.parse_arsenal(REPO)
    assert len(entries) > 50
    names = {e["name"] for e in entries}
    assert {"subfinder", "nuclei"} <= names


def test_collect_inventory_and_undocumented(tmp_path):
    repo = _fake_repo(tmp_path)
    inv = sa.collect_inventory(repo, which=lambda name: "/usr/bin/nmap" if name == "nmap" else None)
    assert set(inv["skills"]) == {"alpha", "beta"}
    assert "hunt.md" in inv["commands"]
    assert {t["name"] for t in inv["external_installed"]} == {"nmap"}
    assert {t["name"] for t in inv["external_missing"]} == {"ffuf"}
    # bar.py is a real tool but not in the README; _private.py is exempt.
    assert inv["undocumented_tools"] == ["bar.py"]


def test_detect_gaps_reports_missing_and_undocumented(tmp_path):
    inv = sa.collect_inventory(_fake_repo(tmp_path), which=lambda _n: None)
    kinds = {g["kind"] for g in sa.detect_gaps(inv)}
    assert "missing_external" in kinds
    assert "undocumented_tool" in kinds


def test_parse_pytest_summary():
    text = "1285 passed, 2 failed, 1 error, 3 skipped in 15.69s"
    out = sa.parse_pytest_summary(text)
    assert out["passed"] == 1285 and out["failed"] == 2 and out["errors"] == 1
    assert out["skipped"] == 3 and out["total"] == 1291


def test_regression_detection():
    baseline = {"passed": 100, "failed": 0, "errors": 0}
    assert sa.detect_regression({"passed": 100, "failed": 0, "errors": 0}, baseline)["regression"] is False
    assert sa.detect_regression({"passed": 99, "failed": 1, "errors": 0}, baseline)["regression"] is True
    assert sa.detect_regression({"passed": 100, "failed": 0, "errors": 0}, None)["regression"] is False


def test_health_score_weights_components(tmp_path):
    inv = sa.collect_inventory(_fake_repo(tmp_path), which=lambda name: "/x" if name == "nmap" else None)
    # half the external tools present, all real tools documented except bar.py
    score = sa.health_score(inv, {"passed": 10, "failed": 0, "errors": 0, "skipped": 0, "total": 10})
    assert 0 <= score <= 100
    assert sa.health_score(inv, None) <= 100


def test_improvement_ledger_roundtrip_and_deltas(tmp_path):
    home = tmp_path / "sa"
    sa.record_improvement(home, "add spec ingest", {"tests_passed": 1285, "tools": 81})
    entry = sa.record_improvement(home, "harden ingest", {"tests_passed": 1300, "tools": 83})
    assert entry["deltas"]["tests_passed"] == 15
    assert entry["deltas"]["tools"] == 2
    rows = sa.read_ledger(home)
    assert [r["title"] for r in rows] == ["add spec ingest", "harden ingest"]


def test_baseline_file_is_owner_only(tmp_path):
    home = tmp_path / "sa"
    sa.write_baseline(home, {"passed": 5, "failed": 0, "errors": 0, "skipped": 0, "total": 5})
    mode = stat.S_IMODE(os.stat(sa.baseline_path(home)).st_mode)
    assert mode == 0o600
    assert sa.read_baseline(home)["passed"] == 5


def test_cli_audit_json(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sa, "REPO", _fake_repo(tmp_path))
    monkeypatch.setattr(sa, "run_tests", lambda *a, **k: {"passed": 5, "failed": 0, "errors": 0,
                                                          "skipped": 0, "total": 5, "rc": 0})
    rc = sa.main(["--home", str(tmp_path / "sa"), "audit", "--json", "--run-tests"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["capabilities"]["skills"] == 2
    assert out["tests"]["passed"] == 5
    assert out["drift"]["regression"] is False


def test_cli_record_and_ledger(tmp_path, capsys):
    home = tmp_path / "sa"
    assert sa.main(["--home", str(home), "record", "--title", "x", "--metric", "tests_passed=10"]) == 0
    capsys.readouterr()
    assert sa.main(["--home", str(home), "ledger", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert rows[0]["title"] == "x" and rows[0]["metrics"]["tests_passed"] == 10


def test_cli_drift_no_baseline(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sa, "run_tests", lambda *a, **k: {"passed": 1, "failed": 0, "errors": 0,
                                                          "skipped": 0, "total": 1, "rc": 0})
    rc = sa.main(["--home", str(tmp_path / "sa"), "drift"])
    assert rc == 0
    assert "no baseline" in capsys.readouterr().out
