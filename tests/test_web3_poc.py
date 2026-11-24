"""Tests for the Web3 PoC deterministic oracle (forge test)."""

import os
import shutil

import pytest

from tools.verifiers.web3_poc import verify, _walk_status

LAB = os.path.join(os.path.dirname(__file__), "benchmark", "web3_access_control")


def test_walk_status_parses_forge_json():
    sample = {"test/Vault.t.sol": {"VaultExploitTest": {
        "test_anyoneCanMint()": {"status": "Success"},
        "test_other()": {"status": "Failure"},
    }}}
    assert _walk_status(sample, "test_anyoneCanMint") == ["Success"]
    assert _walk_status(sample, "test_other") == ["Failure"]


def test_missing_inputs_skip():
    assert verify({"vuln_class": "web3-poc"}).skipped is True


@pytest.mark.skipif(
    shutil.which("forge") is None or not os.path.isdir(os.path.join(LAB, "lib", "forge-std")),
    reason="forge + forge-std required (run: cd lab && forge install foundry-rs/forge-std)",
)
def test_exploit_poc_confirms_and_absent_test_rejects():
    ok = verify({"vuln_class": "web3-poc", "project_dir": LAB,
                 "test_name": "test_anyoneCanMint"})
    assert ok.confirmed is True
    bad = verify({"vuln_class": "web3-poc", "project_dir": LAB,
                  "test_name": "test_does_not_exist"})
    assert bad.confirmed is False
