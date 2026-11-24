"""Tests for the full-lifecycle target's auth semantics + IDOR confirm.

Fast and stdlib-only (no ffuf/katana): boots tests/benchmark/full_target.py,
asserts the login flow, the anonymous auth-bypass, the sensitive-file leak, and
— the key one — that the two-identity IDOR verifier confirms the BOLA.
"""

import sys
import threading

import pytest
import urllib.request
import urllib.error

sys.path.insert(0, "tests")
from benchmark.full_target import Handler  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402

from tools.verifiers.idor import verify as idor_verify  # noqa: E402
from tools.scope_checker import ScopeChecker  # noqa: E402


@pytest.fixture
def server():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def _get(url, cookie=None):
    req = urllib.request.Request(url)
    if cookie:
        req.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.getheader("Set-Cookie")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), e.getheader("Set-Cookie")


def _login(base, user, pw):
    data = f"username={user}&password={pw}".encode()
    req = urllib.request.Request(base + "/login", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.getheader("Set-Cookie").split(";")[0]


def test_login_sets_session_cookie(server):
    assert _login(server, "alice", "password1").startswith("sess=alice")


def test_anon_admin_is_auth_bypass_marker(server):
    st, body, _ = _get(server + "/admin")
    assert st == 200 and "Admin Panel" in body


def test_env_leaks_secret(server):
    st, body, _ = _get(server + "/.env")
    assert st == 200 and "AWS_ACCESS_KEY_ID" in body and "FLAG{" in body


def test_two_identity_idor_confirms_bola(server):
    ca = _login(server, "alice", "password1")
    cb = _login(server, "bob", "password2")
    # bob (attacker) reads alice's order; victim marker = alice's email
    finding = {"vuln_class": "idor", "victim_object_url": server + "/api/orders/1",
               "attacker_headers": {"Cookie": cb}, "victim_marker": "alice@example.test"}
    res = idor_verify(finding, scope_checker=ScopeChecker(["127.0.0.1"]))
    assert res.confirmed is True
    # control: alice reading her own object is not a cross-tenant break
    own = {"vuln_class": "idor", "victim_object_url": server + "/api/orders/1",
           "attacker_headers": {"Cookie": ca}, "victim_marker": "bob@example.test"}
    assert idor_verify(own, scope_checker=ScopeChecker(["127.0.0.1"])).confirmed is False
