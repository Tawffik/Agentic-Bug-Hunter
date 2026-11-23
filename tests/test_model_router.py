"""Tests for tools/model_router.py — stage tiers + cost accounting."""

from tools import model_router as mr


def test_stage_tiers():
    assert mr.tier_for("recon") == "cheap"
    assert mr.tier_for("parse") == "cheap"
    assert mr.tier_for("exploit_reasoning") == "frontier"
    assert mr.tier_for("falsify") == "frontier"
    assert mr.tier_for("report") == "mid"
    assert mr.tier_for("unknown-stage") == "mid"


def test_choose_prefers_tier_head():
    assert mr.choose("recon") == mr.TIER_MODELS["cheap"][0]
    assert mr.choose("exploit_reasoning") == mr.TIER_MODELS["frontier"][0]


def test_override_and_env_win(monkeypatch):
    assert mr.choose("recon", override="my-model") == "my-model"
    monkeypatch.setenv("BRAIN_MODEL", "env-model")
    assert mr.choose("recon") == "env-model"


def test_available_filter(monkeypatch):
    monkeypatch.delenv("BRAIN_MODEL", raising=False)
    m = mr.choose("recon", available=["glm-5.3-flash"])
    assert m == "glm-5.3-flash"


def test_cost_and_per_solve():
    led = mr.CostLedger()
    c1 = led.record("recon", "deepseek-v4-flash", 1_000_000, 0, solved=False)
    c2 = led.record("exploit_reasoning", "claude-opus-4-8", 0, 1_000_000, solved=True)
    assert abs(c1 - 0.28) < 1e-6
    assert abs(c2 - 75.0) < 1e-6
    assert led.per_solve() == round(led.total_usd / 1, 6)
    assert led.to_dict()["schema"] == "cost-ledger/1"


def test_price_fallback_is_safe():
    assert mr.estimate_cost("unknown-model", 1000, 1000) > 0
