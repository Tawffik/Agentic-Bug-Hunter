"""Sealed capture: opt-in HMAC stamping of verifier traces at the single egress seam.

Uses a throwaway local HTTP server we start ourselves (127.0.0.1). No external target.
"""
import hashlib
import http.server
import importlib.util
import os
import sys
import threading

import pytest

from tools.verifiers import base
from tools.verifiers.seal import CaptureSealer


class _H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"uid=1001(www) marker-abc"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


@pytest.fixture
def server():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _H)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_port}/x"
    srv.shutdown()


@pytest.fixture(autouse=True)
def _reset():
    base.set_sealer(None)
    yield
    base.set_sealer(None)


def test_off_by_default_leaves_fields_empty(server):
    ex, _ = base.fetch(server)
    assert ex.seal == "" and ex.sha256 == "" and ex.content == ""
    assert ex.status == 200


def test_active_sealer_stamps_and_validates(server):
    s = CaptureSealer(key=b"\x01" * 32)
    base.set_sealer(s)
    ex, _ = base.fetch(server, role="test")
    assert ex.seal and ex.role == "test" and "marker-abc" in ex.content
    assert s.valid(ex)


def test_tampering_content_or_role_or_url_breaks_seal(server):
    s = CaptureSealer(key=b"\x02" * 32)
    base.set_sealer(s)
    ex, _ = base.fetch(server, role="test")
    forged = base.HttpExchange(**{**ex.to_dict()})
    forged.content = forged.content + " extra"
    assert not s.valid(forged)
    forged = base.HttpExchange(**{**ex.to_dict()})
    forged.content = "fabricated"
    forged.sha256 = hashlib.sha256(b"fabricated").hexdigest()   # agent recomputes the hash
    assert not s.valid(forged)                                   # but cannot recompute the seal
    forged = base.HttpExchange(**{**ex.to_dict()})
    forged.role = "control"
    assert not s.valid(forged)
    forged = base.HttpExchange(**{**ex.to_dict()})
    forged.url = "http://127.0.0.1:1/other"
    assert not s.valid(forged)


def test_different_key_rejects(server):
    base.set_sealer(CaptureSealer(key=b"\x03" * 32))
    ex, _ = base.fetch(server, role="test")
    assert not CaptureSealer(key=b"\x04" * 32).valid(ex)


def test_out_of_scope_block_is_also_stamped():
    class _NoScope:
        def is_in_scope(self, url):
            return False
    s = CaptureSealer(key=b"\x05" * 32)
    base.set_sealer(s)
    ex, body = base.fetch("http://example.invalid/", scope_checker=_NoScope(), role="test")
    assert body == b"" and ex.status is None and s.valid(ex)


def test_key_file_loading(tmp_path, monkeypatch):
    kf = tmp_path / "k"
    kf.write_text("06" * 32)
    monkeypatch.setenv("ZT_SEAL_KEY_FILE", str(kf))
    a, b = CaptureSealer.from_env(), CaptureSealer(key=bytes.fromhex("06" * 32))
    ex = base.HttpExchange("GET", "http://h/", 200, {}, {}, "s", 0.0)
    a.stamp(ex, "test")
    assert b.valid(ex)


def test_compatible_with_security_research_agent_sealer(server):
    """If the SRA harness is checked out next to this repo, its Sealer must accept our seals."""
    src = os.path.join(os.path.dirname(__file__), "..", "..", "security-research-agent", "src")
    if not os.path.isdir(src):
        pytest.skip("security-research-agent not present")
    sys.path.insert(0, src)
    try:
        from agent_core.harness.seal import Sealer
        from agent_core.harness.contract import Evidence
    except Exception:
        pytest.skip("agent_core not importable")
    finally:
        sys.path.remove(src)
    key = b"\x07" * 32
    base.set_sealer(CaptureSealer(key=key))
    ex, _ = base.fetch(server, role="test")
    e = Evidence("http", ex.url, ex.sha256, ex.content, ex.seal, ex.role)
    assert Sealer(key).valid(e)
