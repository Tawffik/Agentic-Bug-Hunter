"""Tests for engagement contract, exploration ledger, traffic capture (offline)."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bughunter"))

from tools.engagement import Engagement, EngagementError, TokenBucket, TEMPLATE
from tools.exploration_ledger import upsert_asset, mark_covered, uncovered, summary
from tools.traffic_capture import proxy_env, capture_run


def _write(tmp_path, data):
    p = tmp_path / "eng.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return str(p)


# --- engagement contract: fail-closed ---
def test_missing_file_refused(tmp_path):
    with pytest.raises(EngagementError):
        Engagement.load(str(tmp_path / "nope.json"))

def test_pending_status_refused(tmp_path):
    eng = Engagement.load(_write(tmp_path, TEMPLATE))
    assert eng.status == "pending_authorization"
    with pytest.raises(EngagementError):
        eng.require_authorized()

def test_empty_scope_refused(tmp_path):
    bad = dict(TEMPLATE, in_scope=[])
    with pytest.raises(EngagementError):
        Engagement.load(_write(tmp_path, bad))

def test_unknown_keys_refused(tmp_path):
    bad = dict(TEMPLATE, sneaky_new_flag=True)
    with pytest.raises(EngagementError):
        Engagement.load(_write(tmp_path, bad))

def test_authorized_scope_check(tmp_path):
    good = dict(TEMPLATE, status="authorized")
    eng = Engagement.load(_write(tmp_path, good))
    eng.require_authorized()
    sc = eng.scope_checker()
    assert sc.is_in_scope("https://api.example.com/x")
    assert not sc.is_in_scope("https://admin.example.com/x")   # out_of_scope
    assert not sc.is_in_scope("https://evil-example.com/")     # suffix confusion
    assert not sc.is_vuln_class_allowed("dos")                 # no_dos default

def test_wildcard_public_suffix_refused(tmp_path):
    bad = dict(TEMPLATE, status="authorized", in_scope=["*.com"])
    eng = Engagement.load(_write(tmp_path, bad))
    with pytest.raises(Exception):
        eng.scope_checker()

def test_token_bucket_spaces_calls():
    import time
    b = TokenBucket(rate_per_second=50)
    t0 = time.monotonic()
    for _ in range(4):
        b.acquire()
    assert time.monotonic() - t0 >= 3 * (1 / 50) * 0.9

# --- exploration ledger ---
def test_ledger_upsert_cover_uncovered(tmp_path):
    d = str(tmp_path)
    a1 = upsert_asset("t.com", "subdomain", "api.t.com", source="crtsh", directory=d)
    a2 = upsert_asset("t.com", "endpoint", "https://api.t.com/login", directory=d)
    assert a1 != a2
    upsert_asset("t.com", "subdomain", "api.t.com", source="renewal", directory=d)  # dedup
    assert len(uncovered("t.com", directory=d)) == 2
    mark_covered("t.com", a1, run="run-1", directory=d)
    left = uncovered("t.com", directory=d)
    assert len(left) == 1 and left[0]["id"] == a2
    s = summary("t.com", directory=d)
    assert s["assets"] == 2 and s["covered"] == 1 and s["by_kind"]["subdomain"] == 1

def test_ledger_unknown_cover_raises(tmp_path):
    with pytest.raises(KeyError):
        mark_covered("t.com", "deadbeef0000", run="r", directory=str(tmp_path))

def test_ledger_bad_kind_raises(tmp_path):
    with pytest.raises(ValueError):
        upsert_asset("t.com", "nonsense", "x", directory=str(tmp_path))

# --- traffic capture ---
def test_proxy_env_empty_is_noop():
    assert proxy_env("") == {}

def test_proxy_env_matrix():
    env = proxy_env("http://127.0.0.1:8080", "/tmp/ca.pem")
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "ALL_PROXY", "all_proxy", "NODE_USE_ENV_PROXY",
              "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE",
              "GIT_SSL_CAINFO", "NODE_EXTRA_CA_CERTS"):
        assert k in env, k
    assert env["SSL_CERT_FILE"] == "/tmp/ca.pem"

def test_capture_run_records_activity(tmp_path):
    log = str(tmp_path / "act.jsonl")
    code = capture_run([sys.executable, "-c", "print('hi')"], log)
    assert code == 0
    recs = [json.loads(x) for x in open(log, encoding="utf-8")]
    assert [r["kind"] for r in recs] == ["tool_use", "tool_result"]
    assert recs[1]["exit"] == 0 and "hi" in recs[1]["stdout_tail"]
    assert recs[1]["duration_ms"] >= 0
