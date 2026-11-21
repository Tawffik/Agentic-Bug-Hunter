"""Regression tests for the quality-first audit fixes.

Each test pins a defect found during the audit so it cannot silently return:
- swarm scope checker must fail closed, not open
- lead_board.rank_key must tolerate malformed ledger lines
- verifier must not crash on a null exchange in an untrusted bundle
- brain triage/grounding/stream-history must behave for non-Ollama providers
- agent dispatcher must match the real hunt.py API and never falsely trip the
  circuit breaker on tools that have no backend
- HuntMemory must not destroy a corrupt session file
- the agent recon scope filter must cover the same files as hunt.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
PKG = REPO / "bughunter"
TOOLS = PKG / "tools"
for p in (str(PKG), str(TOOLS)):
    if p not in sys.path:
        sys.path.insert(0, p)

import agent  # noqa: E402
import brain  # noqa: E402
import hunt  # noqa: E402
import lead_board  # noqa: E402
import swarm  # noqa: E402
import verifier  # noqa: E402
from agent import HuntMemory, ToolDispatcher  # noqa: E402
from tools.scope_checker import ScopeChecker, ScopeError  # noqa: E402


# ─────────────────────────── swarm: fail closed ────────────────────────────

def test_swarm_scope_checker_raises_on_invalid_pattern():
    with pytest.raises(ScopeError):
        swarm._scope_checker(["*.com"])


def test_swarm_coordinate_aborts_on_invalid_scope(monkeypatch):
    monkeypatch.setattr(swarm.lead_board, "load_ledger", lambda t: [
        {"id": "lb-1", "skill": "hunt-ssrf", "evidence": "https://target.com/x?u=1",
         "status": "new", "priority": "high", "created": "2020-01-01T00:00:00Z"},
    ])
    rep = swarm.coordinate("target.com", scope_domains=["*.com"])
    assert rep["dispatched"] == 0
    assert "error" in rep
    assert "scope" in rep["summary"]["note"].lower()


# ─────────────────────── lead_board: tolerant ranking ──────────────────────

def test_rank_key_tolerates_malformed_ledger_line():
    assert lead_board.rank_key({"id": "x"}) is not None


def test_swarm_survives_malformed_ledger_line(monkeypatch):
    monkeypatch.setattr(swarm.lead_board, "load_ledger", lambda t: [
        {"id": "lb-bad", "skill": "hunt-ssrf", "evidence": "https://t/x", "status": "new"},
    ])
    # no priority/created keys — must not raise before dispatch
    rep = swarm.coordinate("target.com", scope_domains=["target.com"])
    assert isinstance(rep, dict)


# ─────────────────── verifier: untrusted null exchange ─────────────────────

def test_verifier_null_exchange_does_not_crash(tmp_path):
    (tmp_path / "bundle.json").write_text(json.dumps({"schema": "poc-bundle/1", "exchange": None}))
    (tmp_path / "request.http").write_text("GET / HTTP/1.1\r\nHost: x\r\n\r\n")
    bundle = verifier.load_bundle(str(tmp_path))
    assert bundle["exchange"] is not None


# ─────────────────────────── brain: provider parity ────────────────────────

def _bare_brain() -> brain.Brain:
    b = brain.Brain.__new__(brain.Brain)
    b.enabled = True
    b.model = "test-model"
    return b


def test_triage_bare_verdict_does_not_crash(monkeypatch):
    b = _bare_brain()
    monkeypatch.setattr(b, "_stream_fast", lambda *a, **k: "VERDICT:   \nno token")
    verdict, _ = b.triage_finding("finding")
    assert verdict == "UNKNOWN"


def test_stream_history_uses_provider_path_for_cloud(monkeypatch):
    b = _bare_brain()

    class FakeLLM:
        provider = "openai"

    b._llm = FakeLLM()
    captured = {}

    def fake_stream(prompt, label, max_tokens=0):
        captured["prompt"] = prompt
        return "OK"

    monkeypatch.setattr(b, "_stream", fake_stream)
    out = b._stream_history([{"role": "user", "content": "scan me"}], "L", 100)
    assert out == "OK"
    assert "scan me" in captured["prompt"]


def test_grounding_rejects_fabricated_path():
    b = _bare_brain()
    evidence = "GET https://t.example/api/v1/users/1 -> 200"
    report = "## REPORT\nreal https://t.example/api/v1/users/1 also /invented/admin/delete\n"
    assert b._ground_report_output(report, evidence) == "NO_REPORTS"


def test_grounding_keeps_grounded_path():
    b = _bare_brain()
    evidence = "https://t.example/api/v1/users/1"
    report = "## REPORT\nendpoint https://t.example/api/v1/users/1 and /api/v1/users/1\n"
    assert b._ground_report_output(report, evidence) != "NO_REPORTS"


# ────────────────────── agent: dispatcher honesty ──────────────────────────

@pytest.fixture
def memory(tmp_path):
    return HuntMemory(str(tmp_path / "agent_session.json"))


def _checker():
    return ScopeChecker(domains=["target.com", "*.target.com"])


def test_dispatch_run_recon_matches_real_signature(memory, monkeypatch):
    calls = []

    class StrictHunt:
        def run_recon(self, domain, quick=False, scope_lock=False):
            calls.append((domain, quick, scope_lock))
            return True

        def _resolve_recon_dir(self, d):
            return d

    monkeypatch.setattr(agent, "_h", lambda: StrictHunt())
    d = ToolDispatcher("target.com", memory, scope_checker=_checker())
    out = d.dispatch("run_recon", {})
    assert not out.startswith("BLOCKED") and not out.startswith("TOOL UNAVAILABLE")
    assert calls and calls[0][0] == "target.com"


def test_dispatch_run_vuln_scan_matches_real_signature(memory, monkeypatch):
    calls = []

    class StrictHunt:
        def run_vuln_scan(self, domain, quick=False):
            calls.append((domain, quick))
            return True

    monkeypatch.setattr(agent, "_h", lambda: StrictHunt())
    d = ToolDispatcher("target.com", memory, scope_checker=_checker())
    out = d.dispatch("run_vuln_scan", {})
    assert not out.startswith("BLOCKED") and not out.startswith("TOOL UNAVAILABLE")
    assert calls and calls[0][0] == "target.com"


def test_dispatch_unwired_tool_reports_unavailable(memory, monkeypatch):
    monkeypatch.setattr(agent, "_h", lambda: hunt)
    d = ToolDispatcher("target.com", memory, scope_checker=_checker())
    out = d.dispatch("run_secret_hunt", {})
    assert out.startswith("TOOL UNAVAILABLE")


def test_recon_filter_covers_graphql_like_hunt(memory, monkeypatch, tmp_path):
    recon_dir = tmp_path / "recon" / "target.com"
    (recon_dir / "urls").mkdir(parents=True)
    (recon_dir / "urls" / "graphql.txt").write_text(
        "https://evil.example/graphql\nhttps://target.com/graphql\n")

    class FakeHunt:
        _RECON_URL_RELPATHS = hunt._RECON_URL_RELPATHS

        def _resolve_recon_dir(self, d):
            return str(recon_dir)

    monkeypatch.setattr(agent, "_h", lambda: FakeHunt())
    d = ToolDispatcher("target.com", memory, scope_checker=_checker())
    d._filter_recon_urls_to_scope("target.com")
    remaining = (recon_dir / "urls" / "graphql.txt").read_text().splitlines()
    assert remaining == ["https://target.com/graphql"]


def test_phase_tools_map_labels_to_tool_names():
    assert agent.PHASE_TOOLS["recon"] == ("run_recon",)
    assert "run_vuln_scan" in agent.PHASE_TOOLS["scan"]


def test_hunt_memory_backs_up_corrupt_session(tmp_path):
    p = tmp_path / "session.json"
    p.write_text("{ this is not json")
    mem = HuntMemory(str(p))
    assert (tmp_path / "session.json.corrupt").exists()
    mem.findings_log.append({"severity": "high"})
    mem.save()
    saved = json.loads(p.read_text())
    assert saved["findings_log"] == [{"severity": "high"}]


# ─────────────────── agent: request-file host parsing ──────────────────────

def test_request_file_host_absolute_uri_is_seen(tmp_path):
    p = tmp_path / "req.txt"
    p.write_text("GET http://evil.example/ HTTP/1.1\r\nHost: evil.example\r\n\r\n")
    assert ToolDispatcher._parse_request_file_host(str(p)) == "evil.example"


def test_request_file_host_disagreement_refuses(tmp_path):
    p = tmp_path / "req.txt"
    p.write_text("GET http://evil.example/ HTTP/1.1\r\nHost: target.com\r\n\r\n")
    assert ToolDispatcher._parse_request_file_host(str(p)) is None


def test_request_file_host_host_only(tmp_path):
    p = tmp_path / "req.txt"
    p.write_text("GET /x HTTP/1.1\r\nHost: target.com\r\n\r\n")
    assert ToolDispatcher._parse_request_file_host(str(p)) == "target.com"


# ─────────────────────────── brain: robustness ─────────────────────────────

def test_watchdog_status_zero_max_stale_no_crash(capsys):
    b = _bare_brain()
    b.watchdog_status("recon", elapsed=1, file_size=0, stale_count=0, max_stale=0)
    assert True  # reaching here is the assertion


def test_report_gate_tolerates_array_validation(tmp_path):
    b = _bare_brain()
    (tmp_path / "validation.json").write_text("[]")
    ready, note = b._report_gate(str(tmp_path))
    assert ready is False and "NO_REPORTS" in note

