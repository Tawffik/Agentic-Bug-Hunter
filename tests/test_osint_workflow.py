"""Guardrail for the scheduled GitHub OSINT monitor."""
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "osint-monitor.yml"


def test_osint_workflow_is_github_hosted_and_bounded():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "runs-on: ubuntu-latest" in text
    assert "timeout-minutes:" in text
    assert "sengi-" not in text
    assert "github_osint_monitor.py" in text
    assert "GITHUB_TOKEN" in text
    data = yaml.safe_load(text)
    assert "osint" in data["jobs"]
