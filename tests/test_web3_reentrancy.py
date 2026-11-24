"""Tests for web3_evm_hazard_scan REENTRANCY-01 + Foundry drain PoC."""

import os
import shutil
import sys

import pytest

sys.path.insert(0, "bughunter")
from tools.web3_evm_hazard_scan import scan_file  # noqa: E402

FIX = os.path.join(os.path.dirname(__file__), "..", "benchmarks", "fixtures", "web3", "reentrancy")


def _has_re(path):
    return "REENTRANCY-01" in [f.rule for f in scan_file(path, FIX, set())]


@pytest.mark.parametrize("f,expect", [
    ("seen_bad.sol", True), ("unseen_bad.sol", True),
    ("seen_good.sol", False), ("unseen_good.sol", False),
])
def test_reentrancy_detection(f, expect):
    assert _has_re(os.path.join(FIX, f)) is expect


def test_reentrancy_poc_oracle():
    lab = os.path.join(os.path.dirname(__file__), "benchmark", "web3_reentrancy")
    if shutil.which("forge") is None or not os.path.isdir(os.path.join(lab, "lib", "forge-std")):
        pytest.skip("forge + forge-std required")
    from tools.verifiers.web3_poc import verify
    r = verify({"vuln_class": "web3-poc", "project_dir": lab,
                "test_name": "test_reentrancy_drains_bank"})
    assert r.confirmed is True
