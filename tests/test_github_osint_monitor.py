"""Tests for the GitHub OSINT delta monitor (pure logic + mocked API)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"

sys.path.insert(0, str(TOOLS))
import github_osint_monitor as mon  # noqa: E402


def test_security_commit_detection():
    assert mon.is_security_commit("fix: verify OAuth signature")
    assert mon.is_security_commit("Update GitHub Actions workflow")
    assert not mon.is_security_commit("docs: fix typo in README")


def test_diff_new_repo_and_no_change():
    obs = mon.RepoObservation(
        full_name="acme/app",
        html_url="https://github.com/acme/app",
        private=False,
        pushed_at="2026-11-20T00:00:00Z",
        default_branch="main",
        latest_commit="abc123",
        latest_commit_message="fix auth bypass",
    )
    signals = mon.diff_repo(obs, None)
    kinds = {s.kind for s in signals}
    assert "new_repo" in kinds
    assert "new_commit" in kinds
    assert any(s.severity == "high" for s in signals)

    prev = {
        "latest_commit": "abc123",
        "release_tag": "",
        "workflow_hash": "",
        "secret_alerts": 0,
        "dependabot_alerts": 0,
    }
    assert mon.diff_repo(obs, prev) == []


def test_diff_release_workflow_and_alerts():
    obs = mon.RepoObservation(
        full_name="acme/app",
        html_url="https://github.com/acme/app",
        private=False,
        pushed_at="",
        default_branch="main",
        release_tag="v1.2.3",
        workflow_hash="newhash",
        secret_alerts=2,
        dependabot_alerts=1,
    )
    prev = {
        "latest_commit": "",
        "release_tag": "v1.2.2",
        "workflow_hash": "oldhash",
        "secret_alerts": 0,
        "dependabot_alerts": 0,
    }
    kinds = {s.kind for s in mon.diff_repo(obs, prev)}
    assert {"new_release", "workflow_change", "secret_alert", "dependabot_alert"} <= kinds


def test_render_markdown():
    text = mon.render_markdown(
        [mon.Signal("new_commit", "acme/app", "abc fix auth", "https://x", "high")],
        ["acme"],
        "2026-11-20T00:00:00Z",
    )
    assert "GitHub OSINT delta" in text
    assert "acme/app" in text
    assert "LEAD" in text


def test_collect_repo_with_mocked_api(monkeypatch):
    def fake_get(url, token, params=None):
        if url.endswith("/repos/acme/app"):
            return {
                "full_name": "acme/app", "html_url": "https://github.com/acme/app",
                "private": False, "pushed_at": "2026-11-20T00:00:00Z",
                "default_branch": "main", "description": "app",
            }
        if url.endswith("/commits"):
            return [{"sha": "abcdef123456", "commit": {"author": {"date": "2026-11-20T00:00:00Z"},
                                                       "message": "fix: token check"}}]
        if url.endswith("/releases"):
            return [{"tag_name": "v1.0.0", "published_at": "2026-11-19T00:00:00Z"}]
        if url.endswith("/actions/workflows"):
            return {"workflows": [{"path": ".github/workflows/ci.yml", "state": "active", "updated_at": "x"}]}
        if "secret-scanning" in url:
            return [{"number": 1}]
        if "dependabot" in url:
            return [{"number": 1}, {"number": 2}]
        return None

    monkeypatch.setattr(mon, "_get", fake_get)
    obs = mon.collect_repo("acme/app", None)
    assert obs.latest_commit == "abcdef123456"
    assert obs.release_tag == "v1.0.0"
    assert obs.secret_alerts == 1
    assert obs.dependabot_alerts == 2
    assert obs.workflow_hash


def test_help():
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "github_osint_monitor.py"), "--help"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0
    assert "--orgs" in proc.stdout
    assert "--dry-run" in proc.stdout
