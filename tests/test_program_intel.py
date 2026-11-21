"""Program intel: money parsing, score bounds, and mocked API shapes."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import program_intel  # noqa: E402


def test_parse_money():
    assert program_intel.parse_money("$4,243") == 4243
    assert program_intel.parse_money(100) == 100
    assert program_intel.parse_money("n/a") == 0


def test_score_is_bounded():
    low = program_intel.score_program({"avg_bounty_upper": 0, "resolved_reports": 0, "offers_bounties": False})
    high = program_intel.score_program({
        "avg_bounty_upper": 50000, "base_bounty": 50000, "resolved_reports": 1000,
        "offers_bounties": True, "launched_at": "2026-11-01", "state": "open",
        "validation": "1 day",
    })
    assert 0 <= low <= 100
    assert 0 <= high <= 100
    assert high > low


def test_fetch_hackerone_mocked(monkeypatch):
    monkeypatch.setattr(program_intel, "_request", lambda *a, **k: {
        "data": {"team": {"handle": "okg", "name": "OKG", "url": "https://hackerone.com/okg",
                          "offers_bounties": True, "currency": "usd", "base_bounty": 50,
                          "resolved_report_count": 10, "average_bounty_lower_amount": 100,
                          "average_bounty_upper_amount": 500, "launched_at": "2023-03-14T00:00:00Z",
                          "state": "public_mode"}},
    })
    p = program_intel.fetch_hackerone("okg")
    assert p["handle"] == "okg"
    assert p["avg_bounty_upper"] == 500
    assert p["state"] == "public_mode"


def test_fetch_bugcrowd_mocked(monkeypatch):
    monkeypatch.setattr(program_intel, "_request", lambda *a, **k: {
        "rewardedVulnerabilities": 12, "averagePayout": "$4,243", "validationWithin": "5 days",
    })
    p = program_intel.fetch_bugcrowd("acme")
    assert p["resolved_reports"] == 12
    assert p["avg_bounty_upper"] == 4243
    assert p["validation"] == "5 days"


def test_help():
    proc = subprocess.run([sys.executable, str(TOOLS / "program_intel.py"), "--help"],
                          capture_output=True, text=True)
    assert proc.returncode == 0
    assert "--platform" in proc.stdout
    assert "--handle" in proc.stdout
