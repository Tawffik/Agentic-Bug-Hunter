"""Tests for tools/lead_board.py — recon->skill routing + persistent lead ledger.

Covers the contract that matters: every recon signal maps to the right hunt-*
skill, re-ingesting never wipes a lead's status, and the privileged-path router
does not false-positive on keywords that appear inside a query value.
"""

import pytest

import lead_board as lb  # tools/ is on sys.path via tests/conftest.py


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """Point the ledger at a tmp dir so tests never touch real memory/leads/."""
    monkeypatch.setattr(lb, "LEADS_DIR", str(tmp_path / "leads"))
    return tmp_path


def _make_recon(tmp_path, urls):
    rd = tmp_path / "recon"
    (rd / "urls").mkdir(parents=True)
    (rd / "urls" / "all.txt").write_text("\n".join(urls) + "\n")
    return str(rd)


def test_routing_maps_signals_to_skills(isolated):
    rd = _make_recon(isolated, [
        "https://t.example/api/v2/users?id=1001",       # -> hunt-idor
        "https://t.example/graphql",                     # -> hunt-graphql
        "https://t.example/fetch?url=https://internal",  # -> hunt-ssrf
        "https://t.example/static/app.js.map",           # -> hunt-source-leak
        "https://t.example/saml2/acs",                   # -> hunt-saml
        "https://t.example/api/chat",                    # -> hunt-llm-ai
    ])
    skills = {l["skill"] for l in lb.ingest("t.example", rd)}
    for expected in ("hunt-idor", "hunt-graphql", "hunt-ssrf",
                     "hunt-source-leak", "hunt-saml", "hunt-llm-ai"):
        assert expected in skills, f"{expected} not routed; got {sorted(skills)}"


def test_reingest_preserves_status_and_dedups(isolated):
    rd = _make_recon(isolated, ["https://t.example/graphql"])
    leads = lb.ingest("t.example", rd)
    n = len(leads)
    gid = next(l["id"] for l in leads if l["skill"] == "hunt-graphql")

    lb.touch("t.example", gid, "investigating", "introspection open")

    leads2 = lb.ingest("t.example", rd)               # same recon, re-run
    assert len(leads2) == n                            # dedup: no growth
    g = next(l for l in leads2 if l["id"] == gid)
    assert g["status"] == "investigating"              # progress preserved
    assert g["note"] == "introspection open"


def test_privileged_path_not_triggered_by_query_value(isolated):
    # 'dashboard' lives in the query string, not the path -> no auth-bypass lead.
    rd = _make_recon(isolated, ["https://t.example/login?next=/dashboard"])
    skills = {l["skill"] for l in lb.ingest("t.example", rd)}
    assert "hunt-auth-bypass" not in skills
    assert "hunt-open-redirect" in skills              # the real signal here


def test_touch_unknown_lead_is_safe(isolated):
    rd = _make_recon(isolated, ["https://t.example/graphql"])
    lb.ingest("t.example", rd)
    lb.touch("t.example", "lb-doesnotexist", "killed", None)  # must not raise
    leads = lb.load_ledger("t.example")
    assert all(l["status"] != "killed" for l in leads)


def test_path_object_id_and_authz_leads_route_to_idor(isolated):
    rd = isolated / "recon2"
    (rd / "urls").mkdir(parents=True)
    (rd / "urls" / "all.txt").write_text("https://t.example/dashboard\n")
    (rd / "authz").mkdir()
    (rd / "authz" / "leads.txt").write_text("https://t.example/api/orders/12345\n")

    leads = lb.ingest("t.example", str(rd))
    idor = [l for l in leads if l["skill"] == "hunt-idor"]
    assert idor, f"authz lead not routed; got {[l['skill'] for l in leads]}"
    assert any(l["evidence"].endswith("/api/orders/12345") for l in idor)


def test_ingest_reads_ffuf_dirs_json(isolated):
    """Content-discovery output in dirs/*.json must become leads (was dropped)."""
    import json as _json
    rd = isolated / "recon"
    (rd / "urls").mkdir(parents=True)
    (rd / "urls" / "all.txt").write_text("")
    (rd / "dirs").mkdir()
    (rd / "dirs" / "ffuf_x.json").write_text(_json.dumps({
        "config": {"url": "https://t.example/FUZZ"},
        "results": [{"url": "https://t.example/.env", "status": 200},
                    {"url": "https://t.example/.git/config", "status": 200}],
    }))
    skills = {l["skill"] for l in lb.ingest("t.example", str(rd))}
    assert "hunt-source-leak" in skills


def test_content_slug_not_routed_to_ai_or_api(isolated):
    """Real-target regression: content pages with ai/api in the slug are not
    API/LLM endpoints (/services/api-penetration-test-methodology/ etc.)."""
    for u in ("https://h/services/ai-assessment-methodology/",
              "https://h/services/api-penetration-test-methodology/",
              "https://h/operations/ai-usage-guidelines/"):
        skills = {s for s, _, _, _ in lb.route_observation(u, "url")}
        assert "hunt-llm-ai" not in skills, u
        assert "hunt-api-misconfig" not in skills, u


def test_real_api_paths_still_route(isolated):
    for u, want in (("https://h/api/v2/users", "hunt-api-misconfig"),
                    ("https://h/api/chat", "hunt-llm-ai"),
                    ("https://h/api", "hunt-api-misconfig")):
        assert want in {s for s, _, _, _ in lb.route_observation(u, "url")}, u


def test_cdn_tech_not_routed_to_smuggling(isolated):
    """CDNs (Cloudflare/Akamai/Fastly) and plain web servers (nginx/apache) are
    not desync leads; genuine reverse proxies (haproxy/envoy/varnish) are."""
    for line in ("https://h [200] [x] [Cloudflare,Akamai,Fastly]",
                 "https://h [200] [x] [nginx,Apache]"):
        assert "hunt-http-smuggling" not in {
            s for s, _, _, _ in lb.route_observation(line, "tech")}, line
    for line in ("https://h [200] [x] [haproxy]",
                 "https://h [200] [x] [envoy]",
                 "https://h [200] [x] [Varnish]"):
        assert "hunt-http-smuggling" in {
            s for s, _, _, _ in lb.route_observation(line, "tech")}, line


def test_live_word_not_websocket(isolated):
    assert "hunt-websocket" not in {s for s, _, _, _ in lb.route_observation(
        "https://live.tiktok.com", "url")}
    assert "hunt-websocket" in {s for s, _, _, _ in lb.route_observation(
        "https://h/ws", "url")}


def test_nuclei_targets_not_ingested_as_findings(isolated):
    """Nuclei scan TARGET lists must not become leads (they aren't findings)."""
    import json as _j
    rd = isolated / "recon"
    (rd / "urls").mkdir(parents=True)
    (rd / "urls" / "all.txt").write_text("")
    (rd / "nuclei").mkdir()
    (rd / "nuclei" / "targets.txt").write_text("https://t.example/a\nhttps://t.example/b\n")
    (rd / "nuclei" / "findings.jsonl").write_text("")
    assert lb.ingest("t.example", str(rd)) == []


def test_nuclei_jsonl_findings_are_routed(isolated):
    import json as _j
    rd = isolated / "recon"
    (rd / "urls").mkdir(parents=True)
    (rd / "urls" / "all.txt").write_text("")
    (rd / "nuclei").mkdir()
    (rd / "nuclei" / "targets.txt").write_text("https://t.example/a\n")
    (rd / "nuclei" / "findings.jsonl").write_text(_j.dumps({
        "template-id": "ssrf-check", "matched-at": "https://t.example/fetch",
        "info": {"name": "SSRF", "severity": "high", "tags": ["ssrf"]}}) + "\n")
    skills = {l["skill"] for l in lb.ingest("t.example", str(rd))}
    assert "hunt-ssrf" in skills
    assert "hunt-misc" not in skills


def test_pattern_key_collapses_ids_preserves_words(isolated):
    from tools.lead_board import pattern_key
    a = pattern_key("hunt-api-misconfig", "https://t.example/api/v1/share/AIpDsyO0eLhy")[1]
    b = pattern_key("hunt-api-misconfig", "https://t.example/api/v1/share/AJbcd1234abcd")[1]
    assert a == b and a.endswith("/share/<id>")
    # lowercase words and hostnames are NOT collapsed
    assert pattern_key("x", "https://t.example/services/authentication")[1].endswith("/authentication")
    assert "t.example" in pattern_key("x", "https://t.example/api/1")[1]


def test_ingest_merges_near_duplicate_leads(isolated):
    rd = _make_recon(isolated, [
        "https://t.example/api/v1/share/AIpDsyO0eLhy",
        "https://t.example/api/v1/share/AJbcd1234abcd",
        "https://t.example/api/v1/widgets/1001",
        "https://t.example/api/v1/widgets/1002",
    ])
    evs = [l["evidence"] for l in lb.ingest("t.example", rd)]
    assert sum(1 for e in evs if "/share/" in e) == 1
    assert sum(1 for e in evs if "/widgets/" in e) == 1


def test_relative_paths_and_cidrs_not_boarded(isolated):
    from tools.lead_board import _attributable_url
    assert not _attributable_url("/api/v2/pixel")
    assert not _attributable_url("18.208.0.0/13")
    assert not _attributable_url("not a url")
    assert _attributable_url("https://api.t.example/x")
    assert _attributable_url("api.t.example")
    assert _attributable_url("api.t.example:8443/x")


def test_every_routing_label_maps_to_a_real_skill(isolated):
    """The router emits internal hunt-* labels; each must map to a real skill."""
    import pathlib
    root = pathlib.Path(lb.__file__).resolve().parents[2]
    real = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    labels = {r[2] for r in lb.ROUTES if r[2]}
    labels |= {s for _, s in lb.NUCLEI_TAG_SKILL}
    labels.add("hunt-llm-ai")
    unmapped = sorted(l for l in labels if l not in lb.HUNT_SKILL_MAP)
    assert not unmapped, f"routing labels with no skill mapping: {unmapped}"
    for label, skills in lb.HUNT_SKILL_MAP.items():
        assert skills, f"{label} maps to nothing"
        for s in skills:
            assert s in real, f"{label} -> {s}: not a loadable skill"


def test_skills_for_returns_known_targets(isolated):
    assert "graphql-audit" in lb.skills_for("hunt-graphql")
    assert lb.skills_for("hunt-nonexistent") == []


def test_content_pages_not_routed_as_vulns(isolated):
    """Docs/blog/marketing slugs must not become vuln leads (aiven.io case)."""
    rd = _make_recon(isolated, [
        "https://t.example/docs/platform/howto/saml/add-okta-idp",
        "https://t.example/blog/category/ai",
        "https://t.example/resources?type=demo",
        "https://t.example/oauth/authorize",
    ])
    ev = [l["evidence"] for l in lb.ingest("t.example", rd)]
    assert not any("/docs/" in e or "/blog/" in e or "/resources" in e for e in ev), ev
    assert any("/oauth/" in e for e in ev), ev
