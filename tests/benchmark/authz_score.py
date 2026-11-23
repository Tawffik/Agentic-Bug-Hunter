#!/usr/bin/env python3
"""Authz differential benchmark — canary-style recall/precision for /authz-diff.

Boots a two-user target with one real cross-tenant bug and several authorization
controls, then scores the discovery engine and the deterministic IDOR verifier:

  * confirmed recall  — the real BOLA is confirmed by the verifier
  * confirmed FP      — a safe endpoint must never be confirmed
  * marker lead FP    — a safe endpoint must never be classified CROSS_USER_MARKER

The shared-object and per-user endpoints are intentionally present: they are the
cases that fool naive "response length differs / 200 OK" scanners.

Usage:
  python3 tests/benchmark/authz_score.py [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for _path in (_REPO, os.path.join(_REPO, "bughunter")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from tools.authz_diff import Identity, Scanner  # noqa: E402
from tools.scope_checker import ScopeChecker  # noqa: E402

ALICE = "alice@example.test"
BOB = "bob@example.test"
TEAM = "team-42"


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, body: str):
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _who(self) -> str:
        cookie = self.headers.get("Cookie", "")
        if "sess=alice" in cookie:
            return "alice"
        if "sess=bob" in cookie:
            return "bob"
        return "anon"

    def do_GET(self):
        path = self.path.split("?")[0]
        who = self._who()
        if path == "/api/orders/1":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            return self._json(200, {"id": 1, "owner": ALICE, "total": 4242,
                                    "status": "shipped", "address": "1 Main St"})
        if path == "/api/orders/2":
            if who == "alice":
                return self._json(403, {"error": "forbidden"})
            if who == "bob":
                return self._json(200, {"id": 2, "owner": BOB, "total": 777,
                                        "status": "processing", "address": "2 Side St"})
            return self._json(401, {"error": "auth"})
        if path == "/api/me":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            email = ALICE if who == "alice" else BOB
            return self._json(200, {"email": email, "name": who.title(), "plan": "pro"})
        if path == "/api/teams/42":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            return self._json(200, {"team_id": TEAM, "members": 2, "plan": "enterprise"})
        if path == "/api/alice-only":
            if who == "alice":
                return self._json(200, {"role": "admin", "scope": "all", "audit": True})
            if who == "bob":
                return self._json(403, {"error": "forbidden"})
            return self._json(401, {"error": "auth"})
        if path == "/public/status":
            return self._json(200, {"status": "ok", "region": "eu", "build": "2026-11"})
        if path == "/app":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            return self._html("<html><body><div id='root'>Loading application shell</div>"
                              "<script src='/app.js'></script></body></html>")
        return self._json(404, {"error": "not found"})


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


EXPECTED = {
    "/api/orders/1": "CROSS_USER_MARKER",
    "/api/me": "DISTINCT_PER_USER",
    "/api/teams/42": "IDENTICAL_ACROSS_IDENTITIES",
    "/api/alice-only": "ENFORCED",
    "/public/status": "PUBLIC",
    "/app": "SKIPPED",
    "/api/orders/2": "UNKNOWN",
}


def run(port: int | None = None) -> dict:
    httpd = ThreadingHTTPServer(("127.0.0.1", port or _free_port()), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        scanner = Scanner(
            identity_a=Identity("a", {"Cookie": "sess=alice"}),
            identity_b=Identity("b", {"Cookie": "sess=bob"}),
            marker_a=ALICE, marker_b=BOB, delay=0.0,
            scope_checker=ScopeChecker(["127.0.0.1"]), confirm=True,
        )
        results = {}
        for path, expected in EXPECTED.items():
            case = scanner.scan(base + path)
            results[path] = {
                "expected": expected,
                "verdict": case.verdict,
                "confidence": case.confidence,
                "confirmed": bool(case.verifier and case.verifier.get("technically_confirmed")),
                "similarity": round(case.similarity, 3),
            }
    finally:
        httpd.shutdown()

    true_bug = results["/api/orders/1"]
    safe = {p: r for p, r in results.items() if p != "/api/orders/1"}
    confirmed_fp = sum(1 for r in safe.values() if r["confirmed"])
    marker_fp = sum(1 for r in safe.values() if r["verdict"] == "CROSS_USER_MARKER")
    expected_hits = sum(1 for p, r in results.items() if r["verdict"] == EXPECTED[p])
    return {
        "results": results,
        "recall": 1.0 if true_bug["confirmed"] else 0.0,
        "confirmed_fp": confirmed_fp,
        "marker_lead_fp": marker_fp,
        "verdict_accuracy": round(expected_hits / len(EXPECTED), 3),
        "pass": bool(true_bug["confirmed"]) and confirmed_fp == 0 and marker_fp == 0,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Authz differential benchmark")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    report = run()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("Authz differential benchmark")
        for path, result in report["results"].items():
            mark = "✓" if result["verdict"] == result["expected"] else "✗"
            print(f"  [{mark}] {path:20s} expected={result['expected']:28s} "
                  f"got={result['verdict']:28s} confirmed={result['confirmed']}")
        print(f"\n  recall={report['recall']} confirmed_fp={report['confirmed_fp']} "
              f"marker_lead_fp={report['marker_lead_fp']} "
              f"verdict_accuracy={report['verdict_accuracy']}")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
