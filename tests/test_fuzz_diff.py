"""Tests for tools/fuzz_diff.py — per-host baseline response classification."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from tools.fuzz_diff import (classify, dedupe_signals, load_ffuf_hits,
                             normalize_host, fingerprint)


def _hit(status, length, ct="text/html", loc=""):
    return {"url": "https://h/x", "status": status, "length": length,
            "content_type": ct, "location": loc}


def _base(status=404, length=100, ct="text/html"):
    return {"status": status, "length": length, "content_type": ct, "fingerprint": "f"}


def test_unknown_without_baseline():
    assert classify(_hit(200, 500), None)[0] == "UNKNOWN"


def test_spa_fallback_by_fingerprint():
    b = {**_base(200, 500), "fingerprint": fingerprint(b"<html>catch all 123</html>")}
    h = {**_hit(200, 500), "fingerprint": fingerprint(b"<html>catch all 999</html>")}
    assert classify(h, b, body_available=True)[0] == "SPA_FALLBACK"


def test_status_labels():
    assert classify(_hit(401, 10), _base(200, 100))[0] == "AUTH_REQUIRED"
    assert classify(_hit(302, 0), _base(200, 100))[0] == "REDIRECT"
    assert classify(_hit(500, 10), _base(200, 100))[0] == "SERVER_ERROR"
    assert classify(_hit(403, 10), _base(200, 100))[0] == "WAF_BLOCK"
    assert classify(_hit(403, 10), _base(404, 10))[0] == "INTERESTING"


def test_noise_vs_interesting_by_length():
    assert classify(_hit(200, 105), _base(200, 100))[0] == "NOISE"
    assert classify(_hit(200, 400), _base(200, 100))[0] == "INTERESTING"


def test_content_type_change_is_interesting():
    assert classify(_hit(200, 100, ct="application/json"),
                    _base(200, 100, ct="text/html"))[0] == "INTERESTING"


def test_dedupe_repeated_block_pages():
    rows = [
        {"url": "https://h/a", "label": "WAF_BLOCK", "status": 403, "length": 100},
        {"url": "https://h/b", "label": "WAF_BLOCK", "status": 403, "length": 100},
        {"url": "https://h/c", "label": "INTERESTING", "status": 200, "length": 999},
    ]
    out = dedupe_signals(rows)
    assert out[0]["label"] == "WAF_BLOCK"
    assert out[1]["label"] == "DUPLICATE"       # same (status,length)
    assert out[2]["label"] == "INTERESTING"     # distinct signal kept


def test_normalize_host():
    assert normalize_host("https://api.h/x?y=1") == "https://api.h"
    assert normalize_host("nope") is None


def test_load_ffuf_hits_url_and_input(tmp_path):
    p = tmp_path / "f.json"
    p.write_text(json.dumps({"config": {"url": "https://h/FUZZ"},
                             "results": [{"url": "https://h/a", "status": 200, "length": 5},
                                         {"input": {"FUZZ": "b"}, "status": 403, "length": 9}]}))
    hits = load_ffuf_hits([str(p)])
    assert {h["url"] for h in hits} == {"https://h/a", "https://h/b"}


class _CatchAll(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):  # noqa: N802
        body = b"<html>app shell</html>"  # same for every path
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def test_baseline_makes_spa_paths_noise(tmp_path):
    from tools.fuzz_diff import build_baseline, diff
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _CatchAll)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    host = f"http://127.0.0.1:{srv.server_address[1]}"
    try:
        base = build_baseline([host])
        hits = [{"url": host + "/admin", "status": 200,
                 "length": len(b"<html>app shell</html>"), "content_type": "text/html"}]
        out = diff(base, hits)
        assert out[0]["label"] == "NOISE"     # SPA catch-all, not a real hit
    finally:
        srv.shutdown()
