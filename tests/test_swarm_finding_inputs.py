"""Tests for swarm's lead -> finding translation and lead-board routing fixes.

Regression guards for the end-to-end gaps found during the benchmark run:
  - `?url=` observations must route to BOTH SSRF and open-redirect
  - class-appropriate param selection (url-ish vs id-ish)
  - SQLi leads get a standard sleep payload so they don't park
  - NO invented values (no guessed auth-bypass marker, no internal SSRF target)
"""

from tools.swarm import finding_from_lead, _pick_param, _verifier_inputs
from tools.lead_board import route_observation


def test_url_param_routes_to_ssrf_and_redirect():
    text = "http://h/go?url=https://evil.example/"
    skills = {s for s, _, _, _ in route_observation(text, "url")}
    assert "hunt-ssrf" in skills
    assert "hunt-open-redirect" in skills


def test_pick_param_prefers_url_for_redirect():
    assert _pick_param("http://h/go?url=x&id=1", "open-redirect") == "url"


def test_pick_param_prefers_id_for_idor():
    assert _pick_param("http://h/o?a=1&id=5", "idor") == "id"


def test_pick_param_falls_back_to_first():
    assert _pick_param("http://h/o?alpha=1&beta=2", "open-redirect") == "alpha"


def test_sqli_lead_gets_standard_sleep_payload():
    f = finding_from_lead(
        {"id": "lb-1", "skill": "hunt-sqli", "evidence": "http://h/search?q=1"}, "t")
    assert f["param"] == "q"
    assert "SLEEP" in f["sleep_payload"]
    assert f["trials"] >= 1


def test_no_invented_auth_marker_or_ssrf_target():
    ab = finding_from_lead(
        {"id": "lb-1", "skill": "hunt-auth-bypass", "evidence": "http://h/admin"}, "t")
    assert "success_marker" not in ab          # cannot be guessed -> must park
    ssrf = finding_from_lead(
        {"id": "lb-2", "skill": "hunt-ssrf", "evidence": "http://h/f?url=x"}, "t")
    assert "ssrf_target" not in ssrf           # no invented internal target
    assert "metadata" not in str(ssrf).lower()


def test_verifier_inputs_only_sqli():
    assert _verifier_inputs("open-redirect", "http://h/go?next=x") == {}
    assert "sleep_payload" in _verifier_inputs("sqli", "http://h/s?q=1")


def test_class_mapping_gaps_closed():
    from tools.verifiers import normalize_class
    # parked classes that DO have a verifier must map (was: 'no verifier')
    assert normalize_class("llm-ai") == "llm-exfil"
    assert normalize_class("llm ai") == "llm-exfil"
    assert normalize_class("saml") == "xxe"
    # genuinely verifier-less classes stay honest (park, not fake-confirm)
    assert normalize_class("oauth") == ""
    assert normalize_class("mfa-bypass") == ""
