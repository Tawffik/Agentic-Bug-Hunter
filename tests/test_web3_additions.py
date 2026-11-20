"""Contract tests for the Web3 additions: fuzz skill, hazard scanner, corpus search,
multi-chain detection, and pre-audit git analysis."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
SKILL = REPO / "skills" / "web3-fuzz"


def test_web3_fuzz_skill_is_complete():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\nname: web3-fuzz\n")
    assert "Echidna" in text and "Medusa" in text and "Foundry" in text
    assert (SKILL / "LICENSE").exists()
    assert (SKILL / "UPSTREAM.md").exists()
    for path in (
        "templates/Base.sol",
        "templates/FuzzTester.sol",
        "templates/Properties.sol",
        "templates/echidna.yaml",
        "templates/medusa.json",
        "references/property-generation.md",
        "scripts/extract_abis.js",
        "scripts/generate_suite.js",
        "scripts/run_medusa.js",
        "scripts/run_echidna.js",
        "agents/invariant-discovery/conservation-auditor.md",
    ):
        assert (SKILL / path).exists(), f"missing {path}"


def test_web3_fuzz_scripts_are_syntactically_valid():
    for js in (SKILL / "scripts").glob("*.js"):
        proc = subprocess.run(["node", "--check", str(js)], capture_output=True, text=True)
        assert proc.returncode == 0, f"{js}: {proc.stderr}"
    for sh in (SKILL / "scripts").glob("*.sh"):
        proc = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True)
        assert proc.returncode == 0, f"{sh}: {proc.stderr}"


def test_validation_and_preaudit_references_exist():
    base = REPO / "skills" / "web3-audit" / "references"
    for name, needles in {
        "validation-gates.md": ("Gate 1", "Gate 2", "Gate 3", "Gate 4", "confidence"),
        "pre-audit-xray.md": ("Git-history", "Invariants", "xray_git_security.py"),
        "defi-hacklabs.md": ("defi_hack_search.sh", "LEAD"),
    }.items():
        text = (base / name).read_text(encoding="utf-8")
        for needle in needles:
            assert needle.lower() in text.lower(), f"{name} missing {needle}"


def test_multichain_doc_and_tool_exist():
    doc = (REPO / "web3" / "13-multichain-audit.md").read_text(encoding="utf-8")
    for chain in ("Solana", "Aptos Move", "Sui Move", "Soroban", "DAML"):
        assert chain in doc, f"missing {chain}"
    assert "chain_audit_env.sh" in doc
    proc = subprocess.run(["bash", "-n", str(TOOLS / "chain_audit_env.sh")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


def test_chain_audit_env_detects_foundry(tmp_path: Path):
    (tmp_path / "foundry.toml").write_text("[profile.default]\nsrc = 'src'\n", encoding="utf-8")
    proc = subprocess.run(
        ["bash", str(TOOLS / "chain_audit_env.sh"), str(tmp_path), "--json"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["chains"] == ["evm-foundry"]
    assert data["build"] == "forge build"
    assert "tools" in data


def test_defi_hack_search_with_local_fixture(tmp_path: Path):
    (tmp_path / "src" / "test").mkdir(parents=True)
    (tmp_path / "src" / "test" / "Exploit.sol").write_text(
        "// flashloan oracle manipulation\ncontract Exploit {}\n", encoding="utf-8"
    )
    proc = subprocess.run(
        ["bash", str(TOOLS / "defi_hack_search.sh"), "flashloan", "--dir", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Exploit.sol" in proc.stdout
    assert "LEAD-only" in proc.stdout


def test_evm_hazard_scanner_flags_multicall_and_l2(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "Vault.sol").write_text(
        "pragma solidity 0.8.24;\n"
        "contract Vault {\n"
        "  function multicall(bytes[] calldata c) external payable {\n"
        "    for (uint i; i < c.length; i++) { (bool ok,) = address(this).delegatecall(c[i]); require(ok); }\n"
        "  }\n"
        "  function many(uint[] calldata a) external payable {\n"
        "    for (uint i; i < a.length; i++) { require(msg.value >= a[i]); }\n"
        "  }\n"
        "  function l2() external view returns (uint) { return block.number; }\n"
        "}\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "web3_evm_hazard_scan.py"), str(tmp_path), "--json",
         "--chain", "arbitrum", "--chain", "all-l2"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    rules = {item["rule"] for item in json.loads(proc.stdout)}
    assert {"PAYABLE_MULTICALL_LOOP", "MSG_VALUE_IN_LOOP", "L2-ARB-01"} <= rules


def test_xray_git_security_help():
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "xray_git_security.py"), "--help"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0
    assert "--src-dir" in proc.stdout
