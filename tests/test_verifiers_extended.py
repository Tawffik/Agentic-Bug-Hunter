"""Offline tests for the 2026 verifier additions (no network).

Each module imports `fetch` from base, so we monkeypatch the module-local name
and return deterministic HttpExchange/body pairs. This proves each oracle's
confirm/reject logic without touching a target.
"""
import json

from tools.verifiers.base import HttpExchange


def _pair(url, status=200, headers=None, body=b"", method="GET"):
    body = body if isinstance(body, bytes) else body.encode()
    return (HttpExchange(method, url, status, {}, headers or {}, body.decode()[:200], 1.0, ""), body)


# --------------------------------------------------------------------------- CORS

def test_cors_confirms_reflected_origin_with_credentials(monkeypatch):
    import tools.verifiers.cors as mod

    def fake(url, headers=None, **kw):
        return _pair(url, 200, {"Access-Control-Allow-Origin": headers["Origin"],
                                "Access-Control-Allow-Credentials": "true"}, b"{}")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "cors", "url": "https://t/api",
                    "attacker_origin": "https://attacker.example"})
    assert r.confirmed and r.vuln_class == "cors"


def test_cors_rejects_reflection_without_credentials(monkeypatch):
    import tools.verifiers.cors as mod

    def fake(url, headers=None, **kw):
        return _pair(url, 200, {"Access-Control-Allow-Origin": headers["Origin"]}, b"{}")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "cors", "url": "https://t/api"})
    assert not r.confirmed and "credentials" in r.oracle


# ---------------------------------------------------------------- MASS ASSIGNMENT

def test_mass_assignment_confirms_persisted_privileged_field(monkeypatch):
    import tools.verifiers.mass_assignment as mod

    def fake(url, method="GET", headers=None, data=None, **kw):
        payload = json.loads(data) if data else {}
        return _pair(url, 200, {}, json.dumps({"role": payload.get("role", "user")}))

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "mass-assignment", "url": "https://t/me",
                    "field": "role", "value": "ROLE_MARKER_42", "body": {"name": "x"}})
    assert r.confirmed


def test_mass_assignment_rejects_when_baseline_has_marker(monkeypatch):
    import tools.verifiers.mass_assignment as mod

    def fake(url, method="GET", headers=None, data=None, **kw):
        return _pair(url, 200, {}, b"ROLE_MARKER_42")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "mass-assignment", "url": "https://t/me",
                    "field": "role", "value": "ROLE_MARKER_42"})
    assert not r.confirmed


# --------------------------------------------------------------------------- SSTI

def test_ssti_confirms_evaluated_product(monkeypatch):
    import tools.verifiers.ssti as mod

    def fake(url, **kw):
        return _pair(url, 200, {}, b"<h1>total: 6735023</h1>")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "ssti", "url": "https://t/s?q=1", "param": "q"})
    assert r.confirmed


def test_ssti_rejects_literal_reflection(monkeypatch):
    import tools.verifiers.ssti as mod

    def fake(url, **kw):
        return _pair(url, 200, {}, b"you sent {{7393*911}}")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "ssti", "url": "https://t/s?q=1", "param": "q"})
    assert not r.confirmed


# ------------------------------------------------------------------- GRAPHQL IDOR

def test_graphql_idor_confirms_cross_identity_read(monkeypatch):
    import tools.verifiers.graphql_idor as mod

    def fake(url, method="GET", headers=None, data=None, **kw):
        if headers and headers.get("Authorization"):
            return _pair(url, 200, {}, b'{"data":{"user":{"email":"victim@corp.example"}}}')
        return _pair(url, 200, {}, b'{"data":{"user":null}}')

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "graphql-idor", "url": "https://t/graphql",
                    "attacker_headers": {"Authorization": "Bearer A"},
                    "victim_marker": "victim@corp.example", "victim_id": "2"})
    assert r.confirmed


# --------------------------------------------------------------------------- SSRF

def test_ssrf_inband_confirms_internal_marker_only(monkeypatch):
    import tools.verifiers.ssrf as mod

    def fake(url, **kw):
        if "169.254.169.254" in url:
            return _pair(url, 200, {}, b"ami-id: i-123 INTERNAL_MARKER")
        return _pair(url, 200, {}, b"welcome")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "ssrf", "url": "https://t/fetch?url=http://x",
                    "param": "url", "ssrf_target": "http://169.254.169.254/latest/meta-data/",
                    "success_marker": "INTERNAL_MARKER"})
    assert r.confirmed


# ---------------------------------------------------------------------- LLM EXFIL

def test_llm_exfil_confirms_planted_canary(monkeypatch):
    import tools.verifiers.llm_exfil as mod

    def fake(url, method="GET", headers=None, data=None, **kw):
        payload = json.loads(data) if data else {}
        system = (payload.get("system") or "")
        return _pair(url, 200, {}, b"CANARY-9f3a" if "CANARY-9f3a" in system else b"sure!")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "llm-exfil", "url": "https://t/v1/chat",
                    "secret_marker": "CANARY-9f3a"})
    assert r.confirmed


# ----------------------------------------------------------------- BUSINESS LOGIC

def test_business_logic_confirms_scripted_invariant_break(monkeypatch):
    import tools.verifiers.business_logic as mod

    def fake(url, **kw):
        if url.endswith("/account"):
            return _pair(url, 200, {}, b'{"balance": 200}')
        return _pair(url, 200, {}, b'{"ok": true}')

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({
        "vuln_class": "business-logic",
        "steps": [{"method": "POST", "url": "https://t/transfer", "json": {"amt": 100}},
                  {"method": "GET", "url": "https://t/account"}],
        "checks": [{"step": 0, "status": 200}, {"step": 1, "contains": '"balance": 200'}],
    })
    assert r.confirmed


# ------------------------------------------------------------------ CACHE POISON

def test_cache_poison_confirms_cached_marker(monkeypatch):
    import tools.verifiers.cache_poison as mod

    store = {}

    def fake(url, headers=None, **kw):
        headers = headers or {}
        if "X-Forwarded-Host" in headers:
            store[url] = headers["X-Forwarded-Host"]
            return _pair(url, 200, {}, b"poisoned")
        return _pair(url, 200, {}, store.get(url, "").encode() or b"clean")

    monkeypatch.setattr(mod, "fetch", fake)
    r = mod.verify({"vuln_class": "cache-poisoning", "url": "https://t/x?cb=1",
                    "inject_header": "X-Forwarded-Host", "marker_host": "EVILMARK"})
    assert r.confirmed


# --------------------------------------------------------- registry/aliases sanity

def test_new_classes_are_registered_and_callable():
    from tools.verifiers import REGISTRY, normalize_class
    for name in ("cors", "mass-assignment", "ssti", "graphql-idor", "ssrf",
                 "llm-exfil", "business-logic", "cache-poisoning"):
        assert normalize_class(name) == name
        assert callable(REGISTRY[name])
    assert normalize_class("web cache poisoning") == "cache-poisoning"
    assert normalize_class("server side template injection") == "ssti"
    assert normalize_class("graphql idor") == "graphql-idor"


def test_saml_xxe_payloads_generated():
    import base64
    from tools.verifiers import oob
    p = oob.payloads_for("oob.example", "saml")
    assert "saml" in p and p["saml"]
    item = p["saml"][0]
    dec = base64.b64decode(item["payload"]).decode()
    assert item["marker"] in dec and "SYSTEM" in dec and "evil.dtd" in dec


def test_saml_verify_requires_callback_then_confirms():
    from tools.verifiers import oob
    p = oob.payloads_for("oob.example", "saml")
    # no interactions -> skip (no callback means no confirmation)
    r1 = oob.verify({"vuln_class": "saml", "oob_payloads": p, "oob_interactions": []})
    assert r1.skipped is True
    # matching interaction -> confirmed
    m = p["saml"][0]["marker"]
    r2 = oob.verify({"vuln_class": "saml", "oob_payloads": p,
                     "oob_interactions": [{"full-id": m, "protocol": "dns"}]})
    assert r2.confirmed is True
