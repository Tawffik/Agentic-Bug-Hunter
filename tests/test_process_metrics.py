"""Tests for tools/process_metrics.py — evidence-chain scoring."""

from tools.process_metrics import score, stage_credit


def _v(status, confirmed, contract_req=False, contract_ok=False, adv=None):
    return {
        "status": status,
        "technically_confirmed": confirmed,
        "verifier": {"confirmed": confirmed, "skipped": False},
        "contract_required": contract_req,
        "contract_satisfied": contract_ok,
        "adversarial": adv,
    }


def test_rates_and_suppression():
    vals = [
        _v("validated_finding", True),
        _v("scanner_hit", True),                     # suppressed by falsifier
        _v("scanner_hit", False),
    ]
    out = score(vals)
    assert out["technically_confirmed"] == 2
    assert out["report_ready"] == 1
    assert out["grounded_verification_rate"] == 0.5
    assert out["false_positive_suppressed"] == 1


def test_contract_and_adversarial_rates():
    vals = [
        _v("validated_finding", True, True, True,
           {"verdict": "SURVIVES"}),
        _v("scanner_hit", True, True, False,
           {"verdict": "FALSIFIED"}),
        _v("scanner_hit", True, adv={"verdict": "INCONCLUSIVE"}),
    ]
    out = score(vals)
    assert out["contract_required"] == 2 and out["contract_satisfied"] == 1
    assert out["contract_pass_rate"] == 0.5
    assert out["adversarial_runs"] == 3
    assert out["falsified"] == 1
    assert out["falsification_rate"] == round(1 / 3, 4)


def test_empty_batch_is_zero_not_crash():
    out = score([])
    assert out["total"] == 0 and out["grounded_verification_rate"] == 0.0


def test_stage_partial_credit():
    out = stage_credit({"recon": True, "hunt": True, "validate": False, "report": False})
    assert out["completed"] == 2 and out["total"] == 4
    assert out["credit"] == 0.5


def test_stage_credit_weighted():
    out = stage_credit({"recon": True, "report": False}, weights={"recon": 1, "report": 3})
    assert out["credit"] == 0.25
