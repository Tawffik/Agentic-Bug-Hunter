"""Tests for the offline JavaScript bundle analyzer."""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import js_analyzer as ja  # noqa: E402

SAMPLE = """
const API = "/api/v2/orders";
fetch("/api/v1/users/123?expand=all");
const badge = "https://cdn.example.com/logo.png";
const rel = "//cdn.example.com/lib.js";
const key = "AIzaSyA12345678901234567890123456789012";
const aws = "AKIAIOSFODNN7EXAMPLE";
const ghp = "ghp_1234567890abcdefghijklmnopqrstuvwxyz";
const stripe = "sk_live_1234567890abcdefghijkl";
const hook = "https://hooks.slack.com/services/T00000000/B00000000/abcdefghijklmnop";
const jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.abcdefgHIJ";
document.getElementById("x").innerHTML = location.hash;
window.addEventListener("message", (e)=>eval(e.data));
//# sourceMappingURL=app.js.map
"""


def test_extract_paths_strips_query_and_filters_assets():
    paths = ja.extract_paths(SAMPLE)
    assert "/api/v2/orders" in paths
    assert "/api/v1/users/123" in paths
    assert "//cdn.example.com/lib.js" not in paths
    assert not any(p.endswith("logo.png") for p in paths)


def test_extract_params_and_urls():
    assert "expand" in ja.extract_params(SAMPLE)
    urls = ja.extract_urls(SAMPLE)
    assert "https://cdn.example.com/logo.png" in urls


def test_extract_secrets_patterns():
    labels = {f.kind for f in ja.extract_secrets(SAMPLE)}
    assert {"google_api_key", "aws_access_key", "github_token",
            "stripe_secret", "slack_webhook", "jwt"} <= labels


def test_extract_secrets_generic_assignment():
    found = ja.extract_secrets('const api_key = "ABCDEF1234567890";')
    assert any(f.kind == "generic_secret" for f in found)


def test_extract_sinks_counts():
    sinks = ja.extract_sinks(SAMPLE)
    assert sinks.get("eval") == 1
    assert sinks.get("innerHTML") == 1
    assert sinks.get("message_listener") == 1


def test_extract_sourcemaps():
    assert "app.js.map" in ja.extract_sourcemaps(SAMPLE)


def test_analyze_path_aggregates_and_dedupes(tmp_path):
    (tmp_path / "a.js").write_text(SAMPLE)
    (tmp_path / "b.js").write_text(SAMPLE)  # duplicate secrets across files
    result = ja.analyze_path(tmp_path)
    assert result["sources"] == 2
    # secrets deduped on (kind, value)
    assert len(result["secrets"]) == len({(s["kind"], s["value"]) for s in result["secrets"]})
    assert "/api/v2/orders" in result["paths"]


def test_write_outputs(tmp_path):
    result = ja.analyze_text(SAMPLE, "app.js")
    out = ja.write_outputs(result, tmp_path / "js")
    names = set(out["written"])
    assert {"endpoints.txt", "urls.txt", "params.txt", "potential_secrets.txt",
            "sourcemaps.txt", "sinks.json", "analysis.json"} <= names
    assert "/api/v2/orders" in (tmp_path / "js" / "endpoints.txt").read_text()


def test_cli_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(SAMPLE))
    rc = ja.main(["analyze", "-", "--json"])
    assert rc == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["endpoints"] >= 2 and summary["secrets"] >= 5


def test_cli_missing_path(capsys):
    assert ja.main(["analyze", "/no/such/file.js"]) == 2
