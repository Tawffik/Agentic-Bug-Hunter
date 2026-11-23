"""Regression: the evidence import must be warmed before parallel verifier threads.

The benchmark run exposed a real deadlock: swarm workers each triggered the
first import of the `memory` package concurrently, and CPython raised
`_ModuleLock('memory.hunt_journal') deadlock`, which recorded a confirmed
finding as scanner_hit. `validate_core` now imports `memory.evidence` eagerly.
"""

import importlib
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import tools.validate_core as vc


def test_evidence_module_is_warmed_at_import():
    # Importing the gate must pull in the evidence backing module up-front.
    assert "memory.evidence" in sys.modules
    assert vc.EvidenceStore is not None
    assert vc.new_finding_id is not None


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):  # noqa: N802
        if self.path == "/.env":
            body = b"AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\nDB_PASSWORD=hunter2xx\n"
            self.send_response(200)
        else:
            body = b"nope"
            self.send_response(404)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def test_concurrent_gate_calls_do_not_deadlock(tmp_path):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    results = []
    lock = threading.Lock()

    def work(i):
        finding = {"vuln_class": "sensitive-file",
                   "url": f"http://127.0.0.1:{port}/.env", "target": "t"}
        res = vc.verify_finding_programmatic(
            finding, session_dir=str(tmp_path / f"s{i}"), log_research=False)
        with lock:
            results.append(res)

    try:
        threads = [threading.Thread(target=work, args=(i,)) for i in range(12)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)
    finally:
        srv.shutdown()

    assert len(results) == 12
    assert not any(t.is_alive() for t in threads)
    for r in results:
        joined = " ".join(r.get("rejection_reasons", []))
        assert "deadlock" not in joined
        assert "evidence linking failed" not in joined
        assert r.get("status") == "validated_finding"
