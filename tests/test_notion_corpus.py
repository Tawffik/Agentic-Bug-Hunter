from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
NOTION = REPO / "knowledge" / "notion"
def test_notion_sources_present():
    files = sorted(p.name for p in NOTION.glob("bb-*.md"))
    assert len(files) == 7
    assert (NOTION / "INDEX.md").exists()
    for f in files:
        assert f in (NOTION / "INDEX.md").read_text(encoding="utf-8")
