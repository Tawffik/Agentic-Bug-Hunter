"""The consolidated 333-tip corpus must stay complete and indexed."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TIPS = REPO / "knowledge" / "tips"


def test_tips_corpus_is_complete():
    data = json.loads((TIPS / "data" / "tips.json").read_text(encoding="utf-8"))
    assert len(data) == 333
    skills = list((TIPS / "skills").glob("*.md"))
    assert len(skills) == 333
    assert (TIPS / "INDEX.md").exists()
    assert (TIPS / "CATEGORIES.md").exists()
    assert (TIPS / "LICENSE").exists()


def test_tips_corpus_is_referenced():
    text = (REPO / "knowledge" / "README.md").read_text(encoding="utf-8")
    assert "tips/" in text
    assert "333" in text
