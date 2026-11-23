#!/usr/bin/env python3
"""Contract tests: every tool the autonomous agent advertises must be real.

A dead backend previously failed only at dispatch time (11/13 tools returned
TOOL UNAVAILABLE), so the agent's advertised capability silently diverged from
hunt.py. These tests make that class of regression impossible.
"""
from __future__ import annotations

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import agent

LOCAL_TOOLS = {"read_recon_summary", "read_findings_summary",
               "update_working_memory", "finish"}


def test_every_advertised_tool_has_a_dispatch_path():
    missing = sorted(t for t in agent.TOOL_NAMES
                     if t not in agent.ToolDispatcher.TOOL_BACKENDS and t not in LOCAL_TOOLS)
    assert missing == [], f"advertised but undispatched: {missing}"


def test_every_backend_exists_in_hunt_module():
    hunt = agent._h()
    dead = sorted(
        (tool, backend)
        for tool, backend in agent.ToolDispatcher.TOOL_BACKENDS.items()
        if not hasattr(hunt, backend)
    )
    assert dead == [], f"advertised tools with missing hunt.py backend: {dead}"


def test_no_stale_tool_references():
    hunt = agent._h()
    backends = set(agent.ToolDispatcher.TOOL_BACKENDS)
    backend_fns = set(agent.ToolDispatcher.TOOL_BACKENDS.values())
    assert set(agent.TOOL_NAMES) >= backends
    assert set(agent.PHASE_TOOLS["recon"]) <= set(agent.TOOL_NAMES)
    for name, tools in agent.PHASE_TOOLS.items():
        assert set(tools) <= set(agent.TOOL_NAMES), f"phase {name} references unknown tools"
    assert agent.ToolDispatcher.NETWORK_TOOLS <= set(agent.TOOL_NAMES)
    assert set(agent.ToolDispatcher.TOOL_METHODS) <= set(agent.TOOL_NAMES)
    assert all(hasattr(hunt, fn) for fn in backend_fns)


def test_authz_diff_is_advertised_as_safe_read():
    assert "run_authz_diff" in agent.TOOL_NAMES
    assert agent.ToolDispatcher.TOOL_METHODS["run_authz_diff"] == "GET"
    assert "run_authz_diff" in agent.ToolDispatcher.NETWORK_TOOLS
