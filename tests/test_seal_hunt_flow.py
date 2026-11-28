"""verify_finding (the real hunt-flow entry) with ZT_SEAL=1 on a throwaway 127.0.0.1 server."""
import http.server, os, threading, pytest
from tools.verifiers import verify_finding, base


class _H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"DB_PASSWORD=hunter2xyz" if self.path.startswith("/leak") else b"nope"
        self.send_response(200 if self.path.startswith("/leak") else 404)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass


@pytest.fixture
def server():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_port}"
    srv.shutdown()


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    base.set_sealer(None); monkeypatch.delenv("ZT_SEAL", raising=False)
    yield
    base.set_sealer(None)


def F(u): return {"vuln_class": "sensitive-file", "url": u + "/leak", "markers": [r"DB_PASSWORD=\S+"]}


def test_off_by_default_no_seal_no_control(server):
    r = verify_finding(F(server))
    assert r.confirmed and len(r.trace) == 1 and r.trace[0].seal == ""


def test_zt_seal_stamps_test_and_control(server, monkeypatch):
    monkeypatch.setenv("ZT_SEAL", "1")
    r = verify_finding(F(server))
    roles = [e.role for e in r.trace]
    assert r.confirmed and roles == ["test", "control"]
    assert all(base._SEALER.valid(e) for e in r.trace)
    assert r.trace[1].status == 404
