"""Tests for OSINT/exposure hit attribution (host relationship + noise + class)."""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import exposure_attribution as ea  # noqa: E402


def test_hostname_helpers():
    assert ea.normalize_hostname("API.Acme.com.") == "api.acme.com"
    assert ea.hostname_from_url("https://api.acme.com/x?y=1") == "api.acme.com"
    assert ea.hostname_from_url("acme.com:443/path") == "acme.com"
    assert ea.hostname_from_url("not a url") is None
    assert ea.hostname_from_url("") is None


def test_subdomain_label_boundary():
    assert ea.is_subdomain_of("api.acme.com", "acme.com")
    assert ea.is_subdomain_of("acme.com", "acme.com")
    assert not ea.is_subdomain_of("notacme.com", "acme.com")
    assert not ea.is_subdomain_of("acme.com.evil.com", "acme.com")


def test_registrable_domain_two_label_suffix():
    assert ea.registrable_domain("api.acme.co.uk") == "acme.co.uk"
    assert ea.registrable_domain("a.b.acme.com") == "acme.com"


def test_relationship():
    assert ea.relationship("acme.com", "https://acme.com/x")["relationship"] == "DIRECT_HOST"
    assert ea.relationship("acme.com", "https://api.acme.com/x")["relationship"] == "RELATED_SUBDOMAIN"
    assert ea.relationship("acme.com", "https://evil.com/acme")["relationship"] == "INDEX_ONLY"
    assert ea.relationship("acme.com", "not a url")["relationship"] == "UNATTRIBUTED"


def test_detect_noise():
    assert "noise_host" in ea.detect_noise("http://localhost:3000/.env")
    assert "noise_path" in ea.detect_noise("https://acme.com/node_modules/x.js")
    assert "noise_text" in ea.detect_noise("https://x/y", text="apikey=changeme")
    assert ea.detect_noise("https://acme.com/.env") == []


def test_classify_disclosure_classes():
    assert ea.classify_disclosure("https://t/.git/config")["class"] == "VCS_METADATA"
    assert ea.classify_disclosure("https://t/.env")["class"] == "ENV_CONFIG"
    assert ea.classify_disclosure("https://t/backup.sql")["class"] == "BACKUP_DUMP"
    assert ea.classify_disclosure("https://t/app.js.map")["class"] == "SOURCE_MAP"
    assert ea.classify_disclosure("https://t/openapi.json")["class"] == "API_SPEC"
    assert ea.classify_disclosure("https://t/actuator/env")["class"] == "DIAGNOSTIC"
    assert ea.classify_disclosure("https://t/x", text="AKIAIOSFODNN7EXAMPLE")["class"] == "SECRET_LIKE"
    assert ea.classify_disclosure("https://t/x", source="cdx")["class"] == "HISTORICAL_INDEX"
    assert ea.classify_disclosure("https://t/about")["class"] == "GENERIC_PUBLIC"


def test_score_target_env():
    r = ea.score_hit("acme.com", {"url": "https://acme.com/.env"})
    assert r["verdict"] == "TARGET" and r["score"] >= 70
    assert r["confirmed_vulnerability"] is False


def test_score_subdomain_config():
    r = ea.score_hit("acme.com", {"url": "https://api.acme.com/config.json"})
    assert r["verdict"] in ("TARGET", "LIKELY")
    assert r["relationship"] == "RELATED_SUBDOMAIN"


def test_score_noise_localhost_and_example_host():
    assert ea.score_hit("acme.com", {"url": "http://localhost:3000/.env"})["verdict"] == "NOISE"
    assert ea.score_hit("acme.com", {"url": "https://cdn.example.com/app.js.map"})["verdict"] == "NOISE"


def test_score_third_party_github_noise():
    r = ea.score_hit("acme.com", {"url": "https://github.com/u/acme-clone", "snippet": "sample-app demo"})
    assert r["verdict"] == "NOISE"


def test_template_path_demoted():
    r = ea.score_hit("acme.com", {"url": "https://acme.com/node_modules/pkg/.env.example"})
    assert r["verdict"] == "WEAK"


def test_attribute_hits_ranks_dedupes_and_filters():
    hits = [
        {"url": "https://acme.com/.env"},
        {"url": "https://acme.com/.env"},                       # dupe
        {"url": "http://localhost:3000/.env"},                  # noise
        {"url": "https://api.acme.com/backup.sql"},             # target
    ]
    ranked = ea.attribute_hits("acme.com", hits, min_verdict="WEAK")
    urls = [r["url"] for r in ranked]
    assert urls.count("https://acme.com/.env") == 1
    assert ranked[0]["verdict"] == "TARGET"
    assert all(r["verdict"] != "NOISE" for r in ranked)         # filtered out
    # min-verdict=TARGET drops the subdomain LIKELY
    only_target = ea.attribute_hits("acme.com", hits, min_verdict="TARGET")
    assert all(r["verdict"] == "TARGET" for r in only_target)


def test_cli_attribute_stdin(monkeypatch, capsys):
    payload = "\n".join([
        json.dumps({"url": "https://acme.com/.env"}),
        json.dumps({"url": "http://localhost/.env"}),
    ])
    monkeypatch.setattr("sys.stdin", io.StringIO(payload))
    rc = ea.main(["attribute", "--target", "acme.com", "-i", "-", "--min-verdict", "UNRELATED", "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["leads"] >= 1
    assert out["by_verdict"]["NOISE"] >= 1


def test_cli_classify(capsys):
    assert ea.main(["classify", "--url", "https://t/.git/config", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["class"] == "VCS_METADATA"
