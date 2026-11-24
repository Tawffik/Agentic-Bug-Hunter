"""Tests for tools/app_model.py — dedup + object-reference modeling."""

import json

from tools import app_model


def test_normalize_path_collapses_ids():
    assert app_model.normalize_path("/api/users/123/orders") == "/api/users/{id}/orders"
    assert app_model.normalize_path("/u/550e8400-e29b-41d4-a716-446655440000") == "/u/{uuid}"
    assert app_model.normalize_path("/x/:id") == "/x/{id}"
    assert app_model.normalize_path("/a/deadbeefdeadbeef") == "/a/{hash}"


def test_extract_urls_dedups_and_merges_params():
    eps = app_model.extract_from_urls([
        "https://t/api/users/1/orders?page=2",
        "https://t/api/users/2/orders?page=3&sort=asc",
    ])
    assert len(eps) == 1
    ep = next(iter(eps.values()))
    assert ep["key"] == "GET /api/users/{id}/orders"
    names = {p["name"] for p in ep["params"]}
    assert {"page", "sort"} <= names
    assert "{id}" in ep["object_refs"]


def test_object_param_detection():
    assert app_model.is_object_param("user_id")
    assert app_model.is_object_param("tenant")
    assert app_model.is_object_param("account")
    assert not app_model.is_object_param("q")


def test_js_extraction_finds_method_calls_and_paths():
    js = """
      fetch('/api/v1/invoices/42');
      axios.post('/api/v1/invoices', {});
      const u = "/account/settings";
    """
    eps = app_model.extract_from_js(js, "app.js")
    keys = set(eps)
    assert "GET /api/v1/invoices/{id}" in keys
    assert "POST /api/v1/invoices" in keys
    assert "GET /account/settings" in keys


def test_build_reports_stats_and_objects():
    model = app_model.build(
        "acme.com",
        urls=["https://acme.com/api/orders/10", "https://acme.com/api/orders/11"],
        js_texts={"app.js": "fetch('/graphql')"},
    )
    assert model["schema"] == "app-model/1"
    assert model["stats"]["endpoints"] == 2
    assert model["stats"]["object_endpoints"] == 1
    assert any(o["ref"] == "{id}" for o in model["objects"])


def test_spec_ingestion_is_best_effort(tmp_path):
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "t", "version": "1"},
        "paths": {"/users/{userId}": {"get": {"parameters": [
            {"name": "userId", "in": "path", "required": True, "schema": {"type": "string"}}
        ], "responses": {"200": {"description": "ok"}}}}},
    }
    p = tmp_path / "openapi.json"
    p.write_text(json.dumps(spec))
    eps = app_model.extract_from_spec(str(p))
    assert any("{userId}" in k for k in eps)


def test_content_pages_excluded_from_object_surface():
    """Docs/blog content is not an IDOR/object surface (aiven/tiktok case)."""
    m = app_model.build("acme.com", urls=[
        "https://acme.com/blog/howto/{id}",
        "https://acme.com/docs/page/{id}",
        "https://acme.com/api/orders/1",
    ])
    assert m["stats"]["object_endpoints"] == 1
    assert any("/api/orders" in e["key"] for e in m["endpoints"])
