"""Tests for the tool-integrity preflight (shadowed-binary detection)."""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import tool_preflight as tp  # noqa: E402


def _run_returning(text):
    def _run(cmd, **kwargs):
        return types.SimpleNamespace(stdout=text, stderr="", returncode=0)
    return _run


def test_projectdiscovery_httpx_is_ok():
    r = tp.verify_tool("httpx", "projectdiscovery", ["could not run"],
                       which=lambda n: "/go/bin/httpx",
                       run=_run_returning("ProjectDiscovery's HTTP toolkit\nCurrent Version: v1.6.0"))
    assert r["status"] == "OK"


def test_python_httpx_shadow_is_wrong_binary():
    r = tp.verify_tool("httpx", "projectdiscovery", ["could not run", "httpx[cli]"],
                       which=lambda n: "/home/u/.local/bin/httpx",
                       run=_run_returning("The httpx command line client could not run because "
                                          "the required dependencies were not installed. "
                                          "Make sure you've installed everything with: pip install 'httpx[cli]'"))
    assert r["status"] == "WRONG_BINARY"


def test_missing_tool():
    r = tp.verify_tool("naabu", "", [], which=lambda n: None, run=_run_returning(""))
    assert r["status"] == "MISSING"


def test_presence_only_tool_is_ok():
    r = tp.verify_tool("subfinder", "", [], which=lambda n: "/go/bin/subfinder",
                       run=_run_returning("Current Version: v2.17.0"))
    assert r["status"] == "OK"


def test_required_marker_absent_is_unknown():
    r = tp.verify_tool("httpx", "projectdiscovery", [], which=lambda n: "/x/httpx",
                       run=_run_returning("some other program v1"))
    assert r["status"] == "UNKNOWN"


def test_exit_code_wrong_binary_vs_strict():
    wrong = [{"status": "WRONG_BINARY"}]
    missing = [{"status": "MISSING"}]
    ok = [{"status": "OK"}]
    assert tp._exit_code(wrong, strict=False) == 1
    assert tp._exit_code(missing, strict=False) == 0
    assert tp._exit_code(missing, strict=True) == 1
    assert tp._exit_code(ok, strict=True) == 0


def test_preflight_and_cli_json(monkeypatch, capsys):
    tools = [("httpx", "projectdiscovery", ["could not run"]),
             ("subfinder", "", [])]

    def fake_which(n):
        return {"httpx": "/go/bin/httpx", "subfinder": "/go/bin/subfinder"}.get(n)

    def fake_run(cmd, **kwargs):
        text = "ProjectDiscovery" if cmd[0] == "httpx" else "v2"
        return types.SimpleNamespace(stdout=text, stderr="", returncode=0)

    monkeypatch.setattr(tp, "preflight", lambda ts=None, **k: [
        tp.verify_tool(n, m, f, which=fake_which, run=fake_run) for n, m, f in tools])
    rc = tp.main(["--tools", "httpx,subfinder", "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is True and len(out["results"]) == 2
