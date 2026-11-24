"""Tests for tools/api_probe.py — deep API tester + coverage."""

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from tools.api_probe import classify, endpoint_url, build_coverage, run


def test_endpoint_url():
    assert endpoint_url("https://h", "GET /api/x") == "https://h/api/x"
    assert endpoint_url("https://h/", "GET /") == "https://h/"


def test_classify_shell_and_statuses():
    # matches baseline -> bot/SPA shell, never PUBLIC
    assert classify(200, 500, 200, 500) == "BLOCKED_SHELL"
    assert classify(200, 500, 200, 100) == "PUBLIC"
    assert classify(401, 10, 404, 10) == "AUTH_REQUIRED"
    assert classify(302, 0, 404, 10) == "REDIRECT"
    assert classify(500, 10, 404, 10) == "SERVER_ERROR"


def test_classify_methods_and_authz_delta():
    assert classify(200, 100, 404, 10, allow="GET, PUT") == "METHOD_PUT"
    assert classify(200, 100, 404, 10, allow="GET, DELETE") == "METHOD_DELETE"
    # anon allowed but identity denied -> odd delta
    assert classify(200, 100, 404, 10, auth_status=403) == "AUTHZ_DELTA"
    # anon denied, identity allowed -> normal auth required
    assert classify(401, 10, 404, 10, auth_status=200) == "AUTH_REQUIRED"


def test_build_coverage():
    c = build_coverage("t", 3, 10, {"PUBLIC": 3})
    assert c["pct"] == 0.3 and c["tested"] == 3 and c["total"] == 10


class _Srv(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self.send_header("Allow", "GET, POST")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):  # noqa: N802
        p = self.path
        if p == "/public":
            body, st = b"public ok", 200
        elif p == "/private":
            body, st = b"auth required", 401
        else:
            body, st = b"catch-all shell body", 200  # baseline/catch-all
        self.send_response(st)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def test_run_classifies_and_writes_coverage(tmp_path):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Srv)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    host = f"http://127.0.0.1:{srv.server_address[1]}"
    rd = tmp_path / "recon"
    (rd / "urls").mkdir(parents=True)
    (rd / "urls" / "all.txt").write_text(f"{host}/public\n{host}/private\n{host}/unknown\n")
    res = run("t.example", str(rd), max_endpoints=10, out_dir=str(tmp_path / "out"))
    srv.shutdown()
    v = res["coverage"]["by_verdict"]
    assert v.get("PUBLIC", 0) >= 1          # /public
    assert v.get("AUTH_REQUIRED", 0) >= 1   # /private
    assert res["coverage"]["tested"] == 3
    assert (tmp_path / "out" / "coverage.json").is_file()


def test_is_api_endpoint_filter():
    from tools.api_probe import is_api_endpoint
    assert is_api_endpoint("GET /api/orders/1")
    assert is_api_endpoint("POST /v2/users")
    assert is_api_endpoint("GET /graphql")
    assert not is_api_endpoint("GET /some-product-g-601099708851693.html")
    assert not is_api_endpoint("GET /upload_aimg/a.png")
    assert not is_api_endpoint("GET /assets/app.js")


def test_html_shell_detection():
    from tools.api_probe import _is_html_shell, classify
    assert _is_html_shell("text/html", b"<html><script>function _0x24b9(){}") is True
    assert _is_html_shell("application/json", b'{"ok":true}') is False
    # an HTML challenge on an API path is BLOCKED_SHELL, never PUBLIC
    assert classify(200, 500, 404, 10, html_shell=True) == "BLOCKED_SHELL"
