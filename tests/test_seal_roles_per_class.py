"""Per-class roles under ZT_SEAL=1: idor and ssrf capture their own sealed test+control (no extra generic
control), single-probe classes get role=test plus the generic control. Local 127.0.0.1 server only."""
import http.server, threading, pytest
from urllib.parse import urlparse, parse_qs
from tools.verifiers import verify_finding, base

MODE = {"public": False}


class _H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        if self.path.startswith("/obj"):
            ok = self.headers.get("X-User") == "attacker" or MODE["public"]
            body, code = (b"owner=victim secret=VICTIM-DATA", 200) if ok else (b"denied", 403)
        elif self.path.startswith("/fetch"):
            body, code = ((b"META=internal-ok", 200) if "169.254" in (q.get("u") or [""])[0] else (b"ok", 200))
        else:
            body, code = b"nope", 404
        self.send_response(code); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass


@pytest.fixture
def srv():
    s = http.server.HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{s.server_port}"
    s.shutdown()


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    base.set_sealer(None); monkeypatch.setenv("ZT_SEAL", "1"); MODE["public"] = False
    yield
    base.set_sealer(None)


def test_idor_sealed_roles_no_extra_control(srv):
    r = verify_finding({"vuln_class": "idor", "victim_object_url": srv + "/obj/7",
                        "attacker_headers": {"X-User": "attacker"}, "victim_marker": "VICTIM-DATA"})
    assert r.confirmed and [e.role for e in r.trace] == ["test", "control"]
    assert all(base._SEALER.valid(e) for e in r.trace)


def test_idor_public_object_rejected_but_roles_kept(srv):
    MODE["public"] = True
    r = verify_finding({"vuln_class": "idor", "victim_object_url": srv + "/obj/7",
                        "attacker_headers": {"X-User": "attacker"}, "victim_marker": "VICTIM-DATA"})
    assert not r.confirmed and [e.role for e in r.trace] == ["test", "control"] and "VICTIM-DATA" in r.trace[1].content


def test_ssrf_sealed_roles(srv):
    r = verify_finding({"vuln_class": "ssrf", "url": srv + "/fetch?u=x", "param": "u",
                        "ssrf_target": "http://169.254.169.254/", "success_marker": "META=internal-ok",
                        "control_target": "http://example.org/"})
    assert r.confirmed and [e.role for e in r.trace] == ["test", "control"]


def test_single_probe_class_gets_test_plus_generic_control(srv):
    r = verify_finding({"vuln_class": "sensitive-file", "url": srv + "/obj/1", "markers": [r"owner=\w+"]})
    # no X-User header -> 403 -> rejected, but trace is still role-stamped test + control
    assert [e.role for e in r.trace] == ["test", "control"]
