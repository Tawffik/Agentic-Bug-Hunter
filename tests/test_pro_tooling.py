"""Contract tests for the pro workflow pack: browser capture, patch-diff hunting,
installer flag, and external arsenal registration."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
INSTALLER = REPO / "install_tools.sh"
ARSENAL = TOOLS / "external_arsenal.sh"

sys.path.insert(0, str(TOOLS))
import browser_capture  # noqa: E402


def test_browser_capture_pure_parsers():
    assert browser_capture.parse_cookie_string("a=1; b=2") == [
        {"name": "a", "value": "1"},
        {"name": "b", "value": "2"},
    ]
    assert browser_capture.parse_headers(["X-Tenant: 42"]) == {"X-Tenant": "42"}
    redacted = browser_capture.redact_headers(
        {"Authorization": "secret", "Cookie": "session=x", "X-Test": "ok"}
    )
    assert redacted["Authorization"] == "<redacted>"
    assert redacted["Cookie"] == "<redacted>"
    assert redacted["X-Test"] == "ok"


def test_browser_capture_help():
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "browser_capture.py"), "--help"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0
    assert "--storage-state" in proc.stdout
    assert "--har" in proc.stdout


def test_patch_diff_hunt_functional(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    (repo / "Vault.sol").write_text(
        "function withdraw() { require(balance > 0); balance -= 1; }\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "vulnerable"], cwd=repo, check=True)
    (repo / "Vault.sol").write_text(
        "function withdraw() { require(balance > 0); require(msg.sender == owner); balance -= 1; }\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "fix: add owner check"], cwd=repo, check=True)

    out = tmp_path / "out"
    proc = subprocess.run(
        ["bash", str(TOOLS / "patch_diff_hunt.sh"), str(repo), "--out", str(out)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    report = (out / "report.md").read_text(encoding="utf-8")
    assert "Vault.sol" in report
    assert "owner" in report
    assert "Hypotheses to test" in report
    assert (out / "diff.patch").exists()


def test_patch_diff_hunt_syntax():
    proc = subprocess.run(
        ["bash", "-n", str(TOOLS / "patch_diff_hunt.sh")],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_installer_has_pro_flag():
    text = INSTALLER.read_text(encoding="utf-8")
    assert "--with-pro" in text
    assert "INSTALL_PRO=true" in text
    for tool in ("playwright", "awscli", "mitmproxy", "frida-tools", "adb"):
        assert tool in text, f"installer missing {tool}"


def test_arsenal_registers_pro_tools():
    text = ARSENAL.read_text(encoding="utf-8")
    for tool in ("playwright", "aws", "gcloud", "az", "adb", "frida", "mitmproxy"):
        assert f'"{tool}|' in text, f"{tool} missing from arsenal"


def test_pro_commands_exist():
    assert (REPO / "commands" / "browser-capture.md").exists()
    assert (REPO / "commands" / "patch-diff.md").exists()


def test_installer_help_does_not_install():
    proc = subprocess.run(
        ["bash", str(INSTALLER), "--help"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0
    assert "--with-pro" in proc.stdout
    assert "Homebrew not found" not in proc.stdout
    assert "Installing" not in proc.stdout


def test_browser_capture_api_fields():
    from dataclasses import asdict
    from tools.browser_capture import RequestRecord
    r = RequestRecord("POST", "https://h/api/signature", "xhr",
                      post_data='{"tag":"x"}', api_headers={"anti-content": "abc"})
    d = asdict(r)
    assert d["post_data"] == '{"tag":"x"}'
    assert d["api_headers"]["anti-content"] == "abc"
