"""Tests for tools/stage_handoff.py — fresh-context bundles."""

from tools import stage_handoff as sh


def test_build_defaults_per_stage():
    for stage in sh.STAGES:
        b = sh.build(stage, "acme.com")
        assert b["schema"] == sh.SCHEMA
        assert b["stage"] == stage
        assert b["objective"]
        assert any("untrusted" in c.lower() for c in b["constraints"])
        ok, problems = sh.validate(b)
        assert ok, problems


def test_validate_rejects_chain_of_thought():
    b = sh.build("hunt", "acme.com")
    b["chain_of_thought"] = "prior reasoning leaks here"
    ok, problems = sh.validate(b)
    assert ok is False
    assert any("chain_of_thought" in p for p in problems)


def test_validate_rejects_bad_stage():
    b = sh.build("hunt", "acme.com")
    b["stage"] = "nope"
    ok, _ = sh.validate(b)
    assert ok is False


def test_build_accepts_scope_and_inputs():
    b = sh.build("hunt", "acme.com", scope=["*.acme.com"],
                 inputs={"app_model": "recon/app_model.json"})
    assert b["scope"] == ["*.acme.com"]
    assert b["inputs"]["app_model"].endswith("app_model.json")
