"""Tests for tools/parse_ffuf.py — ffuf JSON -> URLs."""

import json

from tools.parse_ffuf import urls_from_ffuf, urls_from_files


def test_url_field_preferred():
    data = {"config": {"url": "http://h/FUZZ"},
            "results": [{"url": "http://h/api/account", "status": 401}]}
    assert urls_from_ffuf(data) == ["http://h/api/account"]


def test_builds_from_input_when_url_absent():
    data = {"config": {"url": "http://h/FUZZ"},
            "results": [{"input": {"FUZZ": "admin"}, "status": 200}]}
    assert urls_from_ffuf(data) == ["http://h/admin"]


def test_ignores_invalid_and_non_http():
    data = {"config": {"url": "http://h/FUZZ"},
            "results": [{"input": {"FUZZ": "x"}}, {"url": "ftp://nope"}, {}]}
    assert urls_from_ffuf(data) == ["http://h/x"]


def test_files_dedup_and_missing(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps({"config": {"url": "http://h/FUZZ"},
                             "results": [{"url": "http://h/x"}, {"url": "http://h/x"}]}))
    b.write_text(json.dumps({"config": {"url": "http://h/FUZZ"},
                             "results": [{"input": {"FUZZ": "y"}}]}))
    urls = urls_from_files([str(a), str(b), str(tmp_path / "missing.json")])
    assert urls == ["http://h/x", "http://h/y"]
