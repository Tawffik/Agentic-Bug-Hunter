#!/usr/bin/env python3
"""Tests for the two-identity authorization differential engine."""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import pytest

from tools.authz_diff import (
    Identity,
    Probe,
    Scanner,
    classify,
    has_object_ref,
    load_identity,
    parse_headers_text,
    similarity,
)
from tools.scope_checker import ScopeChecker

ALICE = "alice@example.test"
BOB = "bob@example.test"

ORDERS = {
    "1": {"id": 1, "owner": ALICE, "total": 4242, "status": "shipped"},
    "2": {"id": 2, "owner": BOB, "total": 777, "status": "processing"},
}


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # silence test output
        pass

    def _send(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _identity(self) -> str:
        cookie = self.headers.get("Cookie", "")
        if "sess=alice" in cookie:
            return "alice"
        if "sess=bob" in cookie:
            return "bob"
        return "anon"

    def do_GET(self):
        path = urlparse(self.path).path
        who = self._identity()

        if path == "/public/status":
            return self._send(200, {"status": "ok", "region": "eu"})

        if path == "/api/me":
            if who == "anon":
                return self._send(401, {"error": "auth"})
            data = {"email": ALICE, "name": "Alice", "plan": "pro"} if who == "alice" \
                else {"email": BOB, "name": "Bob", "plan": "pro"}
            return self._send(200, data)

        if path == "/api/alice-only":
            if who == "alice":
                return self._send(200, {"email": ALICE, "role": "admin", "scope": "all"})
            if who == "bob":
                return self._send(403, {"error": "forbidden"})
            return self._send(401, {"error": "auth"})

        if path.startswith("/api/orders/"):
            oid = path.rsplit("/", 1)[-1]
            order = ORDERS.get(oid)
            if who == "anon":
                return self._send(401, {"error": "auth"})
            if not order:
                return self._send(404, {"error": "not found"})
            if who == "bob" and order["owner"] != BOB:
                return self._send(200, order)
            if who == "alice" and order["owner"] != ALICE:
                return self._send(403, {"error": "forbidden"})
            return self._send(200, order)

        return self._send(404, {"error": "not found"})


@pytest.fixture(scope="module")
def server():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def _scanner(base: str, **kwargs) -> Scanner:
    scope = ScopeChecker(["127.0.0.1"])
    return Scanner(
        identity_a=Identity("a", {"Cookie": "sess=alice"}),
        identity_b=Identity("b", {"Cookie": "sess=bob"}),
        scope_checker=scope,
        delay=0.0,
        **kwargs,
    )


def test_has_object_ref_detects_ids_and_ignores_versions():
    assert has_object_ref("https://app.test/api/orders/12345")
    assert has_object_ref("https://app.test/api?user_id=987")
    assert has_object_ref("https://app.test/users/550e8400-e29b-41d4-a716-446655440000/profile")
    assert not has_object_ref("https://app.test/api/v2/search?q=shoes")
    assert not has_object_ref("https://app.test/dashboard")


def test_parse_headers_storage_state_and_lines():
    state = json.dumps({
        "cookies": [
            {"name": "sess", "value": "alice", "domain": "app.test", "path": "/"},
            {"name": "lang", "value": "en", "domain": "app.test", "path": "/"},
        ],
        "origins": [],
    })
    assert parse_headers_text(state)["Cookie"] == "sess=alice; lang=en"
    assert parse_headers_text("Authorization: Bearer x\nX-Tenant: 7") == {
        "Authorization": "Bearer x", "X-Tenant": "7",
    }
    assert parse_headers_text('{"Cookie": "a=1"}') == {"Cookie": "a=1"}


def test_load_identity_redacts_in_preview(tmp_path):
    path = tmp_path / "b.json"
    path.write_text(json.dumps({"Cookie": "sess=bob"}))
    ident = load_identity("b", str(path))
    assert ident.headers == {"Cookie": "sess=bob"}
    assert ident.redacted() == {"name": "b", "headers": ["Cookie"]}


def _p(status: int, payload) -> Probe:
    body = json.dumps(payload).encode() if not isinstance(payload, bytes) else payload
    return Probe(status=status, body=body, content_type="application/json", length=len(body))


def test_classify_cross_user_marker_beats_similarity():
    a = _p(200, {"id": 1, "owner": ALICE, "total": 4242})
    b = _p(200, {"id": 1, "owner": ALICE, "total": 4242})
    anon = _p(401, {"error": "auth"})
    case = classify(url="https://app.test/api/orders/1", a=a, b=b, anon=anon, marker_a=ALICE)
    assert case.verdict == "CROSS_USER_MARKER"
    assert case.confidence == "high" and case.marker_match


def test_classify_public_control():
    a = _p(200, {"status": "ok", "region": "eu"})
    b = _p(200, {"status": "ok", "region": "eu"})
    anon = _p(200, {"status": "ok", "region": "eu"})
    case = classify(url="https://app.test/public/status", a=a, b=b, anon=anon)
    assert case.verdict == "PUBLIC"
    assert case.confidence == "none"


def test_classify_enforced_for_attacker():
    a = _p(200, {"role": "admin", "scope": "all"})
    b = _p(403, {"error": "forbidden"})
    anon = _p(401, {"error": "auth"})
    case = classify(url="https://app.test/api/alice-only", a=a, b=b, anon=anon)
    assert case.verdict == "ENFORCED"


def test_classify_distinct_per_user_markers():
    a = _p(200, {"email": ALICE, "name": "Alice", "plan": "pro"})
    b = _p(200, {"email": BOB, "name": "Bob", "plan": "pro"})
    anon = _p(401, {"error": "auth"})
    case = classify(
        url="https://app.test/api/me", a=a, b=b, anon=anon,
        marker_a=ALICE, marker_b=BOB,
    )
    assert case.verdict == "DISTINCT_PER_USER"
    assert case.similarity > 0.5


def test_json_similarity_is_shape_aware():
    same_a = _p(200, {"id": 1, "owner": ALICE, "total": 4242})
    same_b = _p(200, {"id": 1, "owner": ALICE, "total": 4242})
    other = _p(200, {"id": 2, "owner": BOB, "total": 777})
    value_same, schema_same = similarity(same_a, same_b)
    value_other, schema_other = similarity(same_a, other)
    assert value_same > 0.99 and schema_same == 1.0
    assert schema_other == 1.0 and value_other < value_same


def test_integration_idor_confirmed_public_enforced_and_me(server):
    scanner = _scanner(server, marker_a=ALICE, marker_b=BOB, confirm=True)
    cases = {
        url: scanner.scan(url)
        for url in (
            f"{server}/api/orders/1",
            f"{server}/api/orders/2",
            f"{server}/api/alice-only",
            f"{server}/api/me",
            f"{server}/public/status",
        )
    }
    vuln = cases[f"{server}/api/orders/1"]
    assert vuln.verdict == "CROSS_USER_MARKER"
    assert vuln.verifier and vuln.verifier["technically_confirmed"] is True
    assert vuln.verifier["status"] == "validated_finding"

    assert cases[f"{server}/api/orders/2"].verdict == "UNKNOWN"
    assert cases[f"{server}/api/alice-only"].verdict == "ENFORCED"
    assert cases[f"{server}/api/me"].verdict == "DISTINCT_PER_USER"
    assert cases[f"{server}/public/status"].verdict == "PUBLIC"


def test_integration_similarity_only_without_marker(server):
    scanner = _scanner(server)
    case = scanner.scan(f"{server}/api/orders/1")
    assert case.verdict == "IDENTICAL_ACROSS_IDENTITIES"
    assert case.confidence == "high"
    assert case.verifier is None


def test_results_are_redacted(tmp_path, server):
    from tools.authz_diff import _write_results

    scanner = _scanner(server, marker_a=ALICE)
    case = scanner.scan(f"{server}/api/orders/1")
    results = _write_results(str(tmp_path), [case], {"identity_b": {"name": "b"}})
    text = open(results, encoding="utf-8").read()
    assert "sess=bob" not in text and "sess=alice" not in text
    assert "CROSS_USER_MARKER" in text


def test_similarity_survives_deeply_nested_json():
    deep = '{"a":' * 2000 + '1' + '}' * 2000
    probe = Probe(status=200, body=deep.encode(), content_type="application/json",
                  length=len(deep))
    value, schema = similarity(probe, probe)
    assert 0.0 <= value <= 1.0 and 0.0 <= schema <= 1.0
