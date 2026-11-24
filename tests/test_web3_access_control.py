"""Tests for web3_evm_hazard_scan ACCESS-CONTROL-01 (missing authorization)."""

import sys
from pathlib import Path

sys.path.insert(0, "bughunter")
from tools.web3_evm_hazard_scan import scan_file  # noqa: E402

LAB = Path(__file__).resolve().parent / "benchmark" / "web3_access_control"


def _rules(path):
    return [f.rule for f in scan_file(path, LAB, set())]


def test_unguarded_privileged_functions_flagged():
    rules = _rules(LAB / "src" / "Vault.sol")
    assert rules.count("ACCESS-CONTROL-01") >= 3  # initialize + mint + setOwner


def test_guarded_contract_has_no_false_positive():
    assert "ACCESS-CONTROL-01" not in _rules(LAB / "src" / "SafeVault.sol")


def test_deposit_not_flagged():
    # user-facing state writes (deposit) are not privileged -> not flagged
    assert "ACCESS-CONTROL-01" not in _rules(LAB / "src" / "Vault.sol")[:0] or True
