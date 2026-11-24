"""Tests for tools/skill_registry.py — skills lifecycle + knowledge coverage."""

from tools import lead_board
from tools.skill_registry import (parse_frontmatter, load_registry, coverage,
                                  index, audit)


def test_frontmatter_block_scalar():
    fm = parse_frontmatter("---\nname: x\ndescription: >\n  a long\n  folded line\n---\nbody")
    assert fm["description"] == "a long folded line"


def test_registry_loads_corpus():
    reg = load_registry()
    assert len(reg) >= 25
    for name, e in reg.items():
        assert e["description"] and len(e["description"]) >= 40, name
        assert e["path"].endswith("SKILL.md")


def test_coverage_no_dangling_targets():
    cov = coverage()
    assert cov["dangling_targets"] == []
    # every routing label maps to >=1 present skill
    for label, v in cov["labels_map"].items():
        assert v["present"], f"{label} has no present skill"
        for s in v["present"]:
            assert s in load_registry()


def test_coverage_matches_lead_board_labels():
    cov = coverage()
    assert set(cov["labels_map"]) == set(lead_board.HUNT_SKILL_MAP)


def test_audit_is_clean_and_reports_reference_integrity():
    issues = audit()
    assert issues == [], issues


def test_index_is_cheap_seed():
    idx = index()
    assert idx and all("name" in e and "description" in e for e in idx)


def test_quality_scorecard():
    from tools.skill_registry import quality
    q = quality()
    assert q["skills"] >= 25
    assert isinstance(q["overlaps"], list)
    assert all("jaccard" in o for o in q["overlaps"])
    assert all(m["skill"] for m in q["metrics"])


def test_recommendations_are_advisory():
    from tools.skill_registry import recommendations
    recs = recommendations()
    assert isinstance(recs, list)
    for r in recs:
        assert r["skill"] and r["recommend"]
