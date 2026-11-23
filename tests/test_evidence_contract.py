"""Tests for tools/evidence_contract.py — the four-part reportability bar."""

from tools.evidence_contract import assess, enforce
from tools.verifiers.base import VerifyResult


def _confirmed(trace=True):
    return VerifyResult(True, "idor", "oracle fired", [], "ok") if not trace \
        else VerifyResult(True, "idor", "oracle fired", [], "ok")


def test_contract_satisfied_for_proven_non_access_class():
    c = assess({"vuln_class": "xss", "url": "https://t/x"}, _confirmed())
    assert c["satisfied"] is True
    assert c["parts"]["proof"] and c["parts"]["artifact"]


def test_contract_requires_ownership_for_access_class():
    f = {"vuln_class": "idor", "url": "https://t/x"}
    c = assess(f, _confirmed())
    assert c["satisfied"] is False
    assert c["parts"]["ownership"] is False
    assert any("ownership" in m for m in c["missing"])


def test_contract_satisfied_when_two_identities_present():
    f = {"vuln_class": "idor", "url": "https://t/x",
         "attacker_headers": {"Authorization": "A"}, "victim_marker": "victim@x"}
    c = assess(f, _confirmed())
    assert c["satisfied"] is True


def test_contract_unsatisfied_without_proof():
    c = assess({"vuln_class": "xss", "url": "https://t/x"}, None)
    assert c["satisfied"] is False
    assert any("proof" in m for m in c["missing"])


def test_contract_recognizes_bundle_as_proof():
    f = {"vuln_class": "xss", "url": "https://t/x", "poc_bundle": "/tmp/b"}
    c = assess(f, None)
    assert c["parts"]["proof"] is True


def test_report_support_is_advisory_not_gating():
    f = {"vuln_class": "xss", "url": "https://t/x"}  # no impact/severity
    c = assess(f, _confirmed())
    assert c["parts"]["report_support"] is False
    assert c["satisfied"] is True  # advisory only


def test_enforce_returns_tuple():
    ok, c = enforce({"vuln_class": "xss", "url": "https://t/x"}, _confirmed())
    assert ok is True and c["schema"] == "evidence-contract/1"
