"""Contract tests for Web3 tooling registration and MCP configs.

These guard the supply-chain fix: the npm package named ``solidity-audit-mcp`` is a
reserved placeholder. The repo must build it from upstream, never install it from npm.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARSENAL = REPO / "bughunter" / "tools" / "external_arsenal.sh"
INSTALLER = REPO / "install_tools.sh"
MCP_DIR = REPO / "bughunter" / "mcp" / "web3-mcp"
WEB3_DOC = REPO / "web3" / "36-solidity-audit-mcp.md"
RESOURCES = REPO / "skills" / "web3-audit" / "references" / "resources.md"


def test_arsenal_registers_web3_tools():
    text = ARSENAL.read_text(encoding="utf-8")
    for tool in ("forge", "cast", "anvil", "slither", "solc-select", "crytic-compile",
                 "aderyn", "echidna", "medusa", "halmos", "myth", "surya",
                 "heimdall", "wake", "solhint", "solana", "anchor", "surfpool",
                 "foundry-mcp"):
        assert re.search(rf'^\s*"{re.escape(tool)}\|web3\|', text, re.M), f"{tool} missing from arsenal"


def test_arsenal_does_not_recommend_placeholder_package():
    text = ARSENAL.read_text(encoding="utf-8")
    for line in text.splitlines():
        code = line.split("  #", 1)[0]
        if "solidity-audit-mcp" in code and "PLACEHOLDER" not in code.upper():
            assert "npm install" not in code and "npx" not in code, (
                f"placeholder npm package recommended: {line.strip()}"
            )


def test_installer_exposes_web3_flag():
    text = INSTALLER.read_text(encoding="utf-8")
    assert "--with-web3" in text
    assert "INSTALL_WEB3=true" in text
    assert "slither-analyzer" in text
    assert "foundryup" in text
    assert "solidity-audit-mcp" in text  # warning/hint, not npm install


def test_installer_is_syntactically_valid():
    # bash -n is cheap and catches accidental syntax errors in the new block.
    import subprocess
    proc = subprocess.run(["bash", "-n", str(INSTALLER)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


def test_web3_mcp_configs_are_valid_json():
    for name in ("opencode-config.json", "claude-config.json"):
        data = json.loads((MCP_DIR / name).read_text(encoding="utf-8"))
        assert data
    opencode = json.loads((MCP_DIR / "opencode-config.json").read_text(encoding="utf-8"))
    assert "mcp" in opencode
    assert "foundry" in opencode["mcp"]
    assert "solidity-audit" in opencode["mcp"]
    # The published foundry-mcp bin lacks a shebang; invoke it with node.
    assert opencode["mcp"]["foundry"]["command"][0] == "node"
    assert "foundry-mcp/dist/index.js" in opencode["mcp"]["foundry"]["command"][1]
    # Disabled by default until the operator builds/verifies the server.
    assert opencode["mcp"]["solidity-audit"]["enabled"] is False


def test_web3_doc_warns_about_placeholder():
    text = WEB3_DOC.read_text(encoding="utf-8")
    assert "placeholder" in text.lower()
    assert "npm install -g solidity-audit-mcp" not in text
    assert "npx solidity-audit-mcp" not in text
    assert "mariano-aguero/solidity-audit-mcp" in text


def test_resources_reference_exists_and_is_curated():
    text = RESOURCES.read_text(encoding="utf-8")
    for source in ("Solodit", "Immunefi", "DeFiHackLabs", "SWC", "Foundry Book",
                   "Sealevel Attacks", "Building Secure Contracts"):
        assert source in text, f"missing resource: {source}"