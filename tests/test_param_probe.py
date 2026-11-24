"""Tests for tools/param_probe.py — built-in hidden-parameter discovery."""

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from tools.param_probe import response_changed, discover, _with_param


def test_with_param_preserves_existing_query():
    out = _with_param("http://h/p?a=1", "q", "x")
    assert "a=1" in out and "q=x" in out


def test_response_changed_status():
    c, why = response_changed(200, b"abc", 500, b"abc", "zzq")
    assert c and "status" in why


def test_response_changed_canary_reflection():
    c, why = response_changed(200, b"<h2></h2>", 200, b"<h2>zzqdeadbeef</h2>", "zzqdeadbeef")
    assert c and why == "canary reflected"


def test_response_changed_length_band():
    c, _ = response_changed(200, b"x" * 1000, 200, b"x" * 1400, "zzq")
    assert c
    c2, _ = response_changed(200, b"x" * 1000, 200, b"x" * 1010, "zzq")
    assert not c2  # within the noise band


def test_identical_is_unchanged():
    c, why = response_changed(200, b"same", 200, b"same", "zzq")
    assert not c and why == ""


def test_error_signature_signal():
    c, why = response_changed(200, b"<h2>0 results</h2>", 200,
                              b"SQL syntax error near ''", "zzq")
    assert c and "error signature" in why


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # noqa: D401
        pass

    def do_GET(self):  # noqa: N802
        p = urlparse(self.path)
        q = parse_qs(p.query)
        headers = {}
        if p.path == "/echo":
            body = f"<h2>{q.get('q', [''])[0]}</h2>".encode()
            status = 200
        elif p.path == "/plain":
            body, status = b"static page", 200
        elif p.path == "/redir":  # redirect param: 302 always, Location from ?to=
            body, status = b"", 302
            headers["Location"] = q.get("to", ["/"])[0]
        elif p.path == "/err":  # error param: quote triggers a 500
            val = q.get("x", [""])[0]
            if "'" in val:
                body, status = b"SQL syntax error near ''", 500
            else:
                body, status = b"ok results", 200
        else:
            body, status = b"nope", 404
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _serve():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv


def test_discover_finds_reflected_param_only():
    srv = _serve()
    port = srv.server_address[1]
    try:
        hits = discover([f"http://127.0.0.1:{port}/echo",
                         f"http://127.0.0.1:{port}/plain"],
                        params=["q", "foo"])
    finally:
        srv.shutdown()
    params = {(h["url"], h["param"]) for h in hits}
    assert (f"http://127.0.0.1:{port}/echo", "q") in params
    # /plain never changes -> nothing discovered for it
    assert not any("/plain" in u for u, _ in params)


def test_discover_finds_redirect_param_via_location():
    srv = _serve()
    port = srv.server_address[1]
    try:
        hits = discover([f"http://127.0.0.1:{port}/redir"], params=["to"])
    finally:
        srv.shutdown()
    assert any(h["param"] == "to" for h in hits)


def test_discover_finds_error_param_via_breaker():
    srv = _serve()
    port = srv.server_address[1]
    try:
        hits = discover([f"http://127.0.0.1:{port}/err"], params=["x"])
    finally:
        srv.shutdown()
    assert any(h["param"] == "x" for h in hits)
