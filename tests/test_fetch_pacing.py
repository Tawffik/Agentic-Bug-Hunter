"""Per-host pacing in verifiers.base.fetch. Fake clock: no real sleeping. Local server only."""
import http.server, threading, pytest
from tools.verifiers import base


class _H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass


@pytest.fixture
def server():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_port}/x"
    srv.shutdown()


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    base.set_pacer(None); monkeypatch.delenv("ZT_RATE_PER_MIN", raising=False)
    yield
    base.set_pacer(None)


class Clk:
    def __init__(self): self.t = 100.0; self.sleeps = []
    def now(self): return self.t
    def sleep(self, d): self.sleeps.append(d); self.t += d


def test_off_by_default_no_wait():
    p = base.HostPacer(0)
    assert p.wait("a") == 0 and p.wait("a") == 0


def test_spacing_per_host():
    c = Clk(); p = base.HostPacer(10, c.now, c.sleep)      # 6 s gap
    assert p.wait("a") == 0
    assert p.wait("a") == pytest.approx(6.0)
    assert p.wait("b") == 0                                  # other host unaffected
    assert p.wait("a") == pytest.approx(6.0)
    assert c.sleeps == [pytest.approx(6.0), pytest.approx(6.0)]


def test_elapsed_time_counts():
    c = Clk(); p = base.HostPacer(10, c.now, c.sleep)
    p.wait("a"); c.t += 4
    assert p.wait("a") == pytest.approx(2.0)


def test_fetch_is_paced(server):
    c = Clk(); base.set_pacer(base.HostPacer(30, c.now, c.sleep))   # 2 s gap
    for _ in range(4):
        ex, _ = base.fetch(server)
        assert ex.status == 200
    assert len(c.sleeps) == 3 and all(s == pytest.approx(2.0) for s in c.sleeps)


def test_env_enables(server, monkeypatch):
    monkeypatch.setenv("ZT_RATE_PER_MIN", "600")
    base.fetch(server); base.fetch(server)
    assert base._PACER is not None and base._PACER.gap == pytest.approx(0.1)
