"""Tests for the bounded exposure-artifact probe.

The network path is intentionally not exercised; every assertion runs against
the pure classifier, URL builder, dry-run planner and scope filter. This keeps
the suite deterministic and prevents accidental outbound requests in CI.
"""

from __future__ import annotations

import json

from tools.exposure_probe import (
    CATALOG,
    ProbeResult,
    build_targets,
    classify_response,
    main,
    run_probe,
)

from tools.scope_checker import ScopeChecker


class TestClassifier:
    def test_git_head_marker_is_lead(self):
        verdict, klass, marker, _ = classify_response(
            "/.git/HEAD", 200, "text/plain", "ref: refs/heads/main\n"
        )
        assert (verdict, klass, marker) == ("LEAD", "VCS_METADATA", "git_head")

    def test_git_config_marker_is_lead(self):
        verdict, klass, _, _ = classify_response(
            "/.git/config", 200, "text/plain", "[core]\n\trepositoryformatversion = 0\n"
        )
        assert verdict == "LEAD"
        assert klass == "VCS_METADATA"

    def test_env_marker_is_lead(self):
        verdict, klass, marker, _ = classify_response(
            "/.env", 200, "text/plain", "APP_ENV=prod\nDB_PASSWORD=s3cr3t\n"
        )
        assert (verdict, klass, marker) == ("LEAD", "ENV_CONFIG_EXPOSURE", "env")

    def test_env_placeholder_is_not_lead(self):
        verdict, klass, _, note = classify_response(
            "/.env", 200, "text/plain", "DB_PASSWORD=changeme\n"
        )
        assert verdict == "UNVERIFIED"
        assert "placeholder" in note

    def test_html_shell_is_suspect_not_lead(self):
        verdict, _, _, _ = classify_response(
            "/.env", 200, "text/html", "<!DOCTYPE html><html><head><title>App</title>"
        )
        assert verdict == "SUSPECT_HTML"

    def test_200_without_marker_is_unverified(self):
        verdict, klass, marker, _ = classify_response(
            "/.env", 200, "application/json", '{"hello":"world"}'
        )
        assert verdict == "UNVERIFIED"
        assert klass == marker == ""

    def test_source_map_marker(self):
        verdict, klass, _, _ = classify_response(
            "/static/app.js.map", 200, "application/json",
            '{"version":3,"sources":["a.ts"],"mappings":"AAAA","sourcesContent":["x"]}',
        )
        assert verdict == "LEAD"
        assert klass == "SOURCE_MAP"

    def test_generic_paths_marker_requires_api_context(self):
        verdict, klass, _, _ = classify_response(
            "/.env", 200, "application/json", '{"paths":["a","b"]}'
        )
        assert verdict == "UNVERIFIED"
        assert klass == ""

    def test_openapi_marker(self):
        verdict, klass, _, _ = classify_response(
            "/openapi.json", 200, "application/json", '{"openapi":"3.0.0","paths":{}}'
        )
        assert verdict == "LEAD"
        assert klass == "API_SPEC"

    def test_actuator_env_marker(self):
        verdict, klass, _, _ = classify_response(
            "/actuator/env", 200, "application/json",
            '{"activeProfiles":["prod"],"propertySources":[]}',
        )
        assert verdict == "LEAD"
        assert klass == "DIAGNOSTIC_SURFACE"

    def test_sql_dump_marker(self):
        verdict, klass, _, _ = classify_response(
            "/dump.sql", 200, "application/sql", "INSERT INTO users (id) VALUES (1);"
        )
        assert verdict == "LEAD"
        assert klass == "BACKUP_DUMP"

    def test_blocked(self):
        assert classify_response("/.env", 403, "", "")[0] == "BLOCKED"
        assert classify_response("/.env", 401, "", "")[0] == "BLOCKED"

    def test_not_present(self):
        assert classify_response("/.env", 404, "", "")[0] == "EMPTY"
        assert classify_response("/.env", 410, "", "")[0] == "EMPTY"

    def test_redirect(self):
        verdict, _, _, note = classify_response("/.env", 302, "text/html", "", "/login")
        assert verdict == "REDIRECT"
        assert "/login" in note

    def test_rate_limit(self):
        assert classify_response("/.env", 429, "", "")[0] == "RATE_LIMIT"

    def test_server_error(self):
        assert classify_response("/.env", 500, "", "")[0] == "ERROR"

    def test_request_failure(self):
        assert classify_response("/.env", 0, "", "")[0] == "ERROR"

    def test_classifier_never_returns_body_values(self):
        secret = "super-secret-value-12345"
        _, _, marker, note = classify_response(
            "/.env", 200, "text/plain", f"DB_PASSWORD={secret}\n"
        )
        assert secret not in marker
        assert secret not in note


class TestBuildTargets:
    def test_joins_paths_onto_base(self):
        targets = build_targets("https://target.com", ["/.env", "actuator/env"])
        assert targets[0] == ("/.env", "https://target.com/.env")
        assert targets[1] == ("actuator/env", "https://target.com/actuator/env")

    def test_adds_scheme_when_missing(self):
        targets = build_targets("target.com", ["/.git/HEAD"])
        assert targets[0][1] == "https://target.com/.git/HEAD"

    def test_strips_path_from_base(self):
        targets = build_targets("https://target.com/some/page", ["/.env"])
        assert targets[0][1] == "https://target.com/.env"

    def test_invalid_base_raises(self):
        try:
            build_targets("   ", ["/.env"])
        except ValueError:
            return
        raise AssertionError("expected ValueError for invalid base URL")


class TestDryRunAndScope:
    def test_dry_run_makes_no_requests(self):
        results = run_probe("https://target.com", ["/.env", "/.git/HEAD"], dry_run=True)
        assert [r.verdict for r in results] == ["PLANNED", "PLANNED"]
        assert all(r.status == 0 for r in results)

    def test_out_of_scope_is_skipped(self):
        checker = ScopeChecker(["*.target.com", "target.com"])
        results = run_probe(
            "https://evil.example", ["/.env"], scope_checker=checker, dry_run=True
        )
        assert results[0].verdict == "SKIPPED"
        assert "out of scope" in results[0].note

    def test_in_scope_is_planned(self):
        checker = ScopeChecker(["*.target.com", "target.com"])
        results = run_probe(
            "https://app.target.com", ["/.env"], scope_checker=checker, dry_run=True
        )
        assert results[0].verdict == "PLANNED"

    def test_main_dry_run_json(self, capsys):
        rc = main(["-u", "https://target.com", "--dry-run", "--json", "--max-paths", "2"])
        assert rc == 0
        out = capsys.readouterr().out.strip().splitlines()
        assert len(out) == 2
        records = [json.loads(line) for line in out]
        assert all(r["verdict"] == "PLANNED" for r in records)
        assert records[0]["url"].startswith("https://target.com/")


class TestCatalogHygiene:
    def test_catalog_is_bounded(self):
        assert 20 <= len(CATALOG) <= 100

    def test_catalog_paths_are_unique(self):
        assert len(CATALOG) == len(set(CATALOG))

    def test_catalog_paths_start_with_slash(self):
        assert all(p.startswith("/") for p in CATALOG)

    def test_probe_result_serializes_without_body(self):
        r = ProbeResult(url="https://t/.env", path="/.env", status=200,
                        content_type="text/plain", verdict="LEAD",
                        disclosure_class="ENV_CONFIG_EXPOSURE", marker="env")
        payload = json.dumps(r.__dict__)
        assert "body" not in payload
        assert "DB_PASSWORD" not in payload