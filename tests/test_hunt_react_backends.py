#!/usr/bin/env python3
"""Offline integration tests for the hunt.py backends the ReAct agent calls."""
from __future__ import annotations

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import pytest

from tools.scope_checker import ScopeChecker


@pytest.fixture
def hunt(tmp_path, monkeypatch):
    import tools.hunt as hunt_mod

    monkeypatch.setattr(hunt_mod, "RECON_DIR", str(tmp_path / "recon"))
    monkeypatch.setattr(hunt_mod, "FINDINGS_DIR", str(tmp_path / "findings"))
    monkeypatch.setattr(hunt_mod, "_SCOPE_CHECKER", None)
    return hunt_mod


def _recon(hunt, domain: str):
    path = os.path.join(hunt.RECON_DIR, domain)
    os.makedirs(path, exist_ok=True)
    return path


def test_run_js_analysis_offline(hunt):
    domain = "example.test"
    js_dir = os.path.join(_recon(hunt, domain), "js")
    os.makedirs(js_dir)
    with open(os.path.join(js_dir, "app.js"), "w") as fh:
        fh.write('fetch("/api/v1/orders/123"); const k="AKIAIOSFODNN7EXAMPLE";')

    assert hunt.run_js_analysis(domain) is True

    out = os.path.join(hunt.FINDINGS_DIR, domain, "js", "js_analysis.txt")
    text = open(out, encoding="utf-8").read()
    assert "/api/v1/orders/123" in text
    assert "aws_access_key" in text


def test_run_js_analysis_without_recon_is_honest(hunt):
    assert hunt.run_js_analysis("empty.test") is False


def test_run_jwt_audit_extracts_token(hunt):
    domain = "jwt.test"
    recon = _recon(hunt, domain)
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwicm9sZSI6ImFkbWluIn0."
        "signaturepart"
    )
    with open(os.path.join(recon, "urls.txt"), "w") as fh:
        fh.write(f"https://app.test/cb?token={token}\n")

    assert hunt.run_jwt_audit(domain) is True

    out = os.path.join(hunt.FINDINGS_DIR, domain, "jwt", "jwt_audit.txt")
    text = open(out, encoding="utf-8").read()
    assert "tokens=1" in text
    assert "HS256" in text or "admin" in text


class _AuthzHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        path = self.path.split("?")[0]
        cookie = self.headers.get("Cookie", "")
        if path == "/api/orders/1":
            if "sess=alice" in cookie:
                body = {"id": 1, "owner": "alice@example.test", "total": 42}
            elif "sess=bob" in cookie:
                body = {"id": 1, "owner": "alice@example.test", "total": 42}
            else:
                self.send_response(401)
                self.end_headers()
                return
            payload = json.dumps(body).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_response(404)
        self.end_headers()


def test_run_authz_diff_end_to_end(hunt, tmp_path, monkeypatch):
    server = ThreadingHTTPServer(("127.0.0.1", 0), _AuthzHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        domain = "127.0.0.1"
        recon = _recon(hunt, domain)
        os.makedirs(os.path.join(recon, "urls"), exist_ok=True)
        url = f"http://127.0.0.1:{server.server_address[1]}/api/orders/1"
        with open(os.path.join(recon, "urls", "with_params.txt"), "w") as fh:
            fh.write(url + "\n")

        a = tmp_path / "a.headers"
        b = tmp_path / "b.headers"
        a.write_text("Cookie: sess=alice\n")
        b.write_text("Cookie: sess=bob\n")
        monkeypatch.setattr(hunt, "_SCOPE_CHECKER", ScopeChecker(["127.0.0.1"]))

        assert hunt.run_authz_diff(
            domain, headers_a=str(a), headers_b=str(b),
            victim_marker="alice@example.test",
        ) is True

        out_dir = os.path.join(hunt.FINDINGS_DIR, domain, "authz")
        result_files = [f for f in os.listdir(out_dir) if f.endswith(".jsonl")]
        assert result_files
        payload = open(os.path.join(out_dir, result_files[0]), encoding="utf-8").read()
        assert "CROSS_USER_MARKER" in payload
        assert "sess=bob" not in payload
    finally:
        server.shutdown()


def test_run_authz_diff_requires_scope(hunt, tmp_path):
    b = tmp_path / "b.headers"
    b.write_text("Cookie: sess=bob\n")
    assert hunt.run_authz_diff("example.test", headers_b=str(b)) is False


def test_run_swarm_uses_argv_not_shell_string(hunt, monkeypatch):
    captured = {}

    def fake_run_cmd(cmd, timeout=600):
        captured["cmd"] = cmd
        captured["timeout"] = timeout
        return True, ""

    monkeypatch.setattr(hunt, "run_cmd", fake_run_cmd)
    monkeypatch.setattr(hunt, "_SCOPE_CHECKER", ScopeChecker(["example.test", "*.example.test"]))
    assert hunt.run_swarm("example.test", workers=3) is True
    cmd = captured["cmd"]
    assert isinstance(cmd, list)
    assert cmd[2] == "example.test"
    assert cmd[-1] == "*.example.test"
    assert "--scope-domain" in cmd


def test_sqlmap_confirmation_ignores_negative_wording(hunt):
    assert hunt._sqlmap_confirmed("Parameter 'id' is vulnerable") is True
    assert hunt._sqlmap_confirmed("all tested parameters do not appear to be injectable") is False
    assert hunt._sqlmap_confirmed("parameter 'id' is not injectable") is False
    assert hunt._sqlmap_confirmed("") is False
