"""Tests for tools/prior_art_rag.py — relevance gating, not blind retrieval."""

from tools.prior_art_rag import search


def _corpus(tmp_path):
    (tmp_path / "a.md").write_text(
        "S3 bucket takeover: dangling CNAME to an unclaimed bucket enables "
        "OAuth redirect abuse and account takeover.\n")
    (tmp_path / "b.md").write_text(
        "GraphQL introspection exposes fields; alias-based IDOR reads another "
        "tenant's object when authorization is missing.\n")
    (tmp_path / "junk.md").write_text("Unrelated cooking notes about pasta.\n")
    return str(tmp_path)


def test_relevant_query_returns_hit(tmp_path):
    out = search("s3 bucket takeover oauth", dirs=[_corpus(tmp_path)], min_overlap=2)
    assert out["gated"] is False
    assert out["results"] and out["results"][0]["path"].endswith("a.md")


def test_irrelevant_query_is_gated(tmp_path):
    out = search("quantum chromodynamics lattice", dirs=[_corpus(tmp_path)], min_overlap=2)
    assert out["gated"] is True
    assert out["results"] == []


def test_empty_query_is_gated(tmp_path):
    out = search("   ", dirs=[_corpus(tmp_path)])
    assert out["gated"] is True


def test_score_floor_can_gate_a_single_overlap(tmp_path):
    # only one query term appears -> min_overlap=2 must block it
    out = search("pasta quantum", dirs=[_corpus(tmp_path)], min_overlap=2)
    assert out["gated"] is True
