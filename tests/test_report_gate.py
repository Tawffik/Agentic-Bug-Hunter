"""Tests for the report gate: nothing unproven (or falsified) can ship.

`is_report_ready` is the single predicate the report path consults. These tests
pin its contract so a future refactor cannot quietly loosen it.
"""

from tools.validate_core import is_report_ready


def _validated(confirmed=True, **extra):
    d = {
        "status": "validated_finding",
        "verifier": {"confirmed": confirmed},
    }
    d.update(extra)
    return d


def test_unproven_is_not_report_ready():
    assert is_report_ready({"status": "scanner_hit",
                            "verifier": {"confirmed": False}}) is False


def test_confirmed_validated_is_report_ready():
    assert is_report_ready(_validated()) is True


def test_missing_verifier_is_not_report_ready():
    assert is_report_ready({"status": "validated_finding"}) is False


def test_strict_contract_unsatisfied_blocks_report():
    d = _validated(contract_required=True, contract_satisfied=False)
    assert is_report_ready(d) is False


def test_strict_contract_satisfied_allows_report():
    d = _validated(contract_required=True, contract_satisfied=True)
    assert is_report_ready(d) is True


def test_falsified_blocks_report_even_if_confirmed():
    d = _validated(adversarial={"verdict": "FALSIFIED", "reasons": ["public"]})
    assert is_report_ready(d) is False


def test_survives_adversarial_allows_report():
    d = _validated(adversarial={"verdict": "SURVIVES", "reasons": []})
    assert is_report_ready(d) is True


def test_non_dict_input_is_not_report_ready():
    assert is_report_ready(None) is False
    assert is_report_ready("x") is False
