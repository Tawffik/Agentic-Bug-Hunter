"""Integration tests for the P0 gates inside validate_core.

These assert the two new hard gates actually change the reportability outcome:
  - strict_contract: unsatisfied evidence contract -> scanner_hit
  - adversarial: FALSIFIED -> scanner_hit (even when the verifier confirmed)
"""

from tools.verifiers.base import VerifyResult
import tools.validate_core as vc


def _confirmed(finding, scope_checker=None):
    return VerifyResult(True, "xss", "oracle fired", [], "ok")


def test_strict_contract_blocks_unreportable(monkeypatch):
    monkeypatch.setattr(vc, "verify_finding", _confirmed)
    res = vc.verify_finding_programmatic(
        {"vuln_class": "xss", "target": "t.example", "strict_contract": True},
        log_research=False,
    )
    assert res["status"] == "scanner_hit"
    assert res["contract_required"] is True
    assert res["contract_satisfied"] is False


def test_strict_contract_allows_reportable(monkeypatch):
    monkeypatch.setattr(vc, "verify_finding", _confirmed)
    res = vc.verify_finding_programmatic(
        {"vuln_class": "xss", "target": "t.example", "url": "https://t.example/x",
         "strict_contract": True},
        log_research=False,
    )
    assert res["status"] == "validated_finding"
    assert res["contract_satisfied"] is True


def test_adversarial_falsified_blocks_report(monkeypatch):
    monkeypatch.setattr(vc, "verify_finding", _confirmed)

    def _falsify(finding, scope_checker=None):
        return {"verdict": "FALSIFIED", "reasons": ["marker is public"], "checks_run": 1}

    import tools.adversarial_validator as av
    monkeypatch.setattr(av, "falsify", _falsify)

    res = vc.verify_finding_programmatic(
        {"vuln_class": "idor", "target": "t.example", "url": "https://t.example/o/2",
         "attacker_headers": {"Authorization": "A"}, "victim_marker": "v@x",
         "adversarial": True},
        log_research=False,
    )
    assert res["status"] == "scanner_hit"
    assert res["adversarial"]["verdict"] == "FALSIFIED"
    assert vc.is_report_ready(res) is False
