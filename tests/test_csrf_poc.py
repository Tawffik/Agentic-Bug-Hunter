"""Tests for the offline CSRF PoC generator and SameSite analyzer."""

from __future__ import annotations

import json

from tools.csrf_poc import analyze_cookie, build_pocs, main


class TestBuildPocs:
    def test_default_variants(self):
        variants = build_pocs("https://target.com/change", {"email": "a@b.c"})
        names = [v.name for v in variants]
        assert names == ["form-urlencoded", "multipart", "method-override-get"]

    def test_form_contains_action_method_and_param(self):
        variants = build_pocs("https://target.com/change", {"email": "a@b.c"})
        html = variants[0].html
        assert 'action="https://target.com/change"' in html
        assert 'method="POST"' in html
        assert 'name="email"' in html
        assert 'value="a@b.c"' in html
        assert "document.forms[0].submit()" in html

    def test_multipart_enctype(self):
        variants = build_pocs("https://target.com/change", {"a": "1"})
        assert 'enctype="multipart/form-data"' in variants[1].html

    def test_token_field_is_included(self):
        variants = build_pocs("https://t/x", {"a": "1"}, token_field="csrf", token_value="ABC")
        assert 'name="csrf"' in variants[0].html
        assert 'value="ABC"' in variants[0].html

    def test_method_override_get(self):
        variants = build_pocs("https://t/x", {"a": "1"}, method="PATCH")
        override = [v for v in variants if v.name == "method-override-get"][0]
        assert 'method="GET"' in override.html
        assert 'name="_method"' in override.html
        assert 'value="PATCH"' in override.html

    def test_json_fetch_variant(self):
        variants = build_pocs("https://t/x", json_body={"email": "a@b.c"})
        v = [x for x in variants if x.name == "json-text-plain"][0]
        assert "fetch(" in v.html
        assert "text/plain" in v.html
        assert "credentials: 'include'" in v.html or 'credentials: "include"' in v.html
        assert "email" in v.html and "a@b.c" in v.html

    def test_graphql_variant(self):
        variants = build_pocs("https://t/graphql", graphql_query="mutation { x }",
                              graphql_variables={"id": 1})
        v = [x for x in variants if x.name == "graphql-form"][0]
        assert 'name="query"' in v.html
        assert 'name="variables"' in v.html
        assert "mutation" in v.html

    def test_html_escaping(self):
        variants = build_pocs('https://t/x?a="b"', {"k": '"<x>'})
        assert "&quot;" in variants[0].html
        assert "&lt;x&gt;" in variants[0].html


class TestCookieAnalysis:
    def test_strict_is_low(self):
        a = analyze_cookie("session=abc; SameSite=Strict; Secure; HttpOnly")
        assert a["samesite"] == "strict"
        assert a["risk"] == "low"
        assert a["secure"] and a["httponly"]

    def test_lax_is_medium_and_mentions_get(self):
        a = analyze_cookie("session=abc; SameSite=Lax")
        assert a["risk"] == "medium"
        assert "GET" in a["note"]

    def test_none_with_secure_is_high(self):
        a = analyze_cookie("session=abc; SameSite=None; Secure")
        assert a["risk"] == "high"

    def test_none_without_secure_is_medium(self):
        a = analyze_cookie("session=abc; SameSite=None")
        assert a["risk"] == "medium"
        assert "Secure" in a["note"]

    def test_absent_samesite_is_high(self):
        a = analyze_cookie("session=abc; HttpOnly")
        assert a["samesite"] == "(absent)"
        assert a["risk"] == "high"

    def test_missing_httponly_note(self):
        a = analyze_cookie("session=abc; SameSite=Lax")
        assert "JS" in a["note"]

    def test_set_cookie_prefix_is_tolerated(self):
        a = analyze_cookie("Set-Cookie: session=abc; SameSite=Strict")
        assert a["samesite"] == "strict"


class TestCli:
    def test_cookie_json(self, capsys):
        rc = main(["--cookie", "session=abc; SameSite=Lax", "--json-out"])
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert data["risk"] == "medium"

    def test_generate_json(self, capsys):
        rc = main(["-u", "https://t/x", "-p", "a=1", "--json-out"])
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert isinstance(data, list) and data[0]["name"] == "form-urlencoded"

    def test_variant_filter(self, capsys):
        rc = main(["-u", "https://t/x", "-p", "a=1", "--variant", "multipart", "--json-out"])
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert [v["name"] for v in data] == ["multipart"]

    def test_out_dir(self, tmp_path, capsys):
        rc = main(["-u", "https://t/x", "-p", "a=1", "--out-dir", str(tmp_path)])
        assert rc == 0
        assert (tmp_path / "form-urlencoded.html").is_file()
        assert (tmp_path / "multipart.html").is_file()