"""Tests for OpenAPI/Swagger/Postman spec ingestion into the attack surface."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "bughunter" / "tools"
sys.path.insert(0, str(TOOLS))
import lead_board as lb  # noqa: E402
import spec_ingest as si  # noqa: E402


@pytest.fixture
def board(tmp_path, monkeypatch):
    monkeypatch.setattr(lb, "LEADS_DIR", str(tmp_path / "leads"))
    return tmp_path


OA = {
    "openapi": "3.1.0",
    "info": {"title": "T", "version": "1"},
    "servers": [{"url": "https://api.example.com/v1"}],
    "security": [{"bearer": []}],
    "paths": {
        "/users/{userId}/orders": {
            "get": {"operationId": "listOrders",
                    "parameters": [{"name": "userId", "in": "path", "required": True}],
                    "responses": {"200": {"description": "ok"}}},
        },
        "/admin/export": {
            "post": {"operationId": "exportAll", "security": [],
                     "requestBody": {"content": {"application/json": {}}},
                     "responses": {"200": {"description": "ok"}}},
        },
        "/files/upload": {
            "post": {"operationId": "upload",
                     "parameters": [{"name": "callbackUrl", "in": "query"}],
                     "responses": {"200": {"description": "ok"}}},
        },
    },
}

SWAGGER = {
    "swagger": "2.0",
    "info": {"title": "S", "version": "1"},
    "host": "legacy.example.com",
    "basePath": "/api",
    "schemes": ["https"],
    "paths": {
        "/orders/{id}": {
            "get": {"operationId": "getOrder",
                    "parameters": [{"name": "id", "in": "path", "required": True}],
                    "responses": {"200": {"description": "ok"}}},
        },
    },
}

POSTMAN = {
    "info": {"name": "P", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
    "item": [
        {"name": "listUsers", "request": {"method": "GET", "url": {"path": ["api", "users"], "query": [{"key": "id"}]}}},
        {"name": "group", "item": [
            {"name": "delUser", "request": {"method": "DELETE", "url": "https://api.example.com/api/users/1",
                                            "auth": {"type": "bearer"}}},
        ]},
    ],
}


def test_detect_and_parse_openapi3():
    kind, eps = si.parse_spec(OA)
    assert kind == "openapi3"
    assert len(eps) == 3
    get = next(e for e in eps if e.method == "GET")
    assert get.url == "https://api.example.com/v1/users/{userId}/orders"


def test_classify_object_reference_idor():
    _, eps = si.parse_spec(OA)
    ep = next(e for e in eps if "users" in e.path)
    skills = {c["skill"] for c in si.classify(ep)}
    assert "hunt-idor" in skills


def test_classify_url_param_ssrf_and_redirect():
    _, eps = si.parse_spec(OA)
    ep = next(e for e in eps if "upload" in e.path)
    skills = {c["skill"] for c in si.classify(ep)}
    assert "hunt-ssrf" in skills
    assert "hunt-open-redirect" in skills
    assert "hunt-file-upload" in skills


def test_classify_admin_and_missing_auth():
    _, eps = si.parse_spec(OA)
    ep = next(e for e in eps if "admin" in e.path)
    skills = {c["skill"] for c in si.classify(ep)}
    assert "hunt-auth-bypass" in skills
    assert "hunt-api-misconfig" in skills


def test_swagger2_base_url():
    kind, eps = si.parse_spec(SWAGGER)
    assert kind == "swagger2"
    assert eps[0].url == "https://legacy.example.com/api/orders/{id}"
    assert "hunt-idor" in {c["skill"] for c in si.classify(eps[0])}


def test_postman_nested_items():
    kind, eps = si.parse_spec(POSTMAN)
    assert kind == "postman"
    assert {e.method for e in eps} == {"GET", "DELETE"}
    delete = next(e for e in eps if e.method == "DELETE")
    assert delete.security == ["postman-auth"]


def test_postman_string_url_is_parsed_not_mangled():
    pm = {"info": {"name": "P", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
          "item": [{"name": "a", "request": {
              "method": "GET", "url": "https://api.example.com/api/users/1?x=1&y=2"}}]}
    _, eps = si.parse_spec(pm)
    ep = eps[0]
    assert ep.path == "/api/users/1"
    assert ep.url == "/api/users/1"
    assert {p.name for p in ep.params} == {"x", "y"}


def test_write_outputs(tmp_path):
    _, eps = si.parse_spec(OA)
    out = si.write_outputs("api.example.com", eps, tmp_path)
    lines = (tmp_path / "api" / "spec_endpoints.txt").read_text().splitlines()
    assert "POST https://api.example.com/v1/admin/export" in lines
    artifact = json.loads((tmp_path / "api" / "spec_findings.json").read_text())
    assert artifact["endpoint_count"] == 3


def test_ingest_to_board_is_idempotent(tmp_path, board):
    _, eps = si.parse_spec(OA)
    classified = si.build_classified(eps)
    added, _ = si.ingest_to_board("api.example.com", classified)
    assert added > 0
    first = len(lb.load_ledger("api.example.com"))
    si.ingest_to_board("api.example.com", classified)
    assert len(lb.load_ledger("api.example.com")) == first


def test_yaml_loading(tmp_path):
    pytest.importorskip("yaml")
    p = tmp_path / "spec.yaml"
    p.write_text("openapi: 3.0.0\ninfo: {title: T, version: '1'}\npaths:\n  /ping:\n    get:\n      responses: {'200': {description: ok}}\n")
    spec = si._load_structured(p)
    kind, eps = si.parse_spec(spec)
    assert kind == "openapi3" and eps[0].path == "/ping"


def test_unknown_spec_rejected():
    with pytest.raises(ValueError):
        si.parse_spec({"foo": "bar"})


def test_cli_json(tmp_path, capsys, board):
    p = tmp_path / "oa.json"
    p.write_text(json.dumps(OA))
    rc = si.main([str(p), "--target", "api.example.com", "--recon-dir", str(tmp_path / "r"), "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["endpoints"] == 3 and out["leads"] > 0
