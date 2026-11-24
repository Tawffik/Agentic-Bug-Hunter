"""Tests for tools/pipeline_plan.py — chunked plan from lead boards."""

from tools.pipeline_plan import build_plan, _lane


def _lead(skill, prio="high", status="new", ev="https://t.example/x"):
    return {"id": "lb-x", "skill": skill, "priority": prio, "status": status, "evidence": ev}


def test_lane_classification():
    assert _lane("hunt-sqli") == "auto"      # has verifier
    assert _lane("hunt-idor") == "authz"     # needs two identities
    assert _lane("hunt-saml") == "auto"      # maps to xxe/oob verifier (parks w/o payloads)
    assert _lane("hunt-oauth") == "ai"       # no verifier


def test_build_plan_chunks_and_orders():
    boards = {
        "t.example": [_lead("hunt-sqli", "high")] * 12 + [_lead("hunt-idor", "high")],
        "u.example": [_lead("hunt-oauth", "med")],
    }
    plan = build_plan(boards, chunk_size=10)
    assert plan["totals"]["leads"] == 14
    # sqli (auto) chunk split into 10 + 2
    autos = [c for c in plan["chunks"] if c["lane"] == "auto"]
    assert sum(c["count"] for c in autos) == 12
    # authz chunk present with correct action
    authz = [c for c in plan["chunks"] if c["lane"] == "authz"]
    assert authz and "authz_diff" in authz[0]["action"]
    # chunk ids assigned
    assert plan["chunks"][0]["chunk_id"] == "chunk-01"


def test_build_plan_skips_touched():
    plan = build_plan({"t.example": [_lead("hunt-sqli", status="killed")]})
    assert plan["chunks"] == []
