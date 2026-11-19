"""Contract tests for the skill corpus.

Every skill is discovered by OpenCode/Pi/Codex from `skills/<name>/SKILL.md`
with YAML frontmatter. A missing `name`/`description`, a name that does not
match its directory, or a relative `.md` link that points nowhere silently
degrades routing or breaks the agent at load time. These tests keep the corpus
discoverable after knowledge-base upgrades.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / "skills"
AGENTS_MD = REPO / "AGENTS.md"

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def skill_files() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def frontmatter(text: str) -> dict[str, str]:
    match = _FRONTMATTER_RE.match(text)
    assert match, "SKILL.md must start with a YAML frontmatter block"
    data: dict[str, str] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value in {">", ">-", "|", "|-", ">+", "|+"}:
            # YAML block scalar: collect indented continuation lines.
            block: list[str] = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            value = " ".join(part for part in block if part)
        data[key] = value
    return data


def test_every_skill_has_discovery_frontmatter():
    files = skill_files()
    assert files, "no skills found"
    for path in files:
        meta = frontmatter(path.read_text(encoding="utf-8"))
        assert meta.get("name"), f"{path}: missing name"
        assert meta.get("description"), f"{path}: missing description"
        assert len(meta["description"]) >= 40, f"{path}: description too short to route on"


def test_skill_name_matches_directory():
    for path in skill_files():
        meta = frontmatter(path.read_text(encoding="utf-8"))
        assert meta["name"] == path.parent.name, (
            f"{path}: name '{meta['name']}' does not match directory '{path.parent.name}'"
        )


def test_skill_descriptions_are_distinct():
    seen: dict[str, Path] = {}
    for path in skill_files():
        meta = frontmatter(path.read_text(encoding="utf-8"))
        desc = meta["description"]
        assert desc not in seen, f"duplicate description: {path} and {seen[desc]}"
        seen[desc] = path


def test_relative_markdown_links_resolve():
    broken: list[str] = []
    for path in skill_files():
        text = path.read_text(encoding="utf-8")
        for match in _LINK_RE.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not target.endswith(".md"):
                continue
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            base = REPO if target.startswith("skills/") else path.parent
            if not (base / target).resolve().is_file():
                broken.append(f"{path.relative_to(REPO)} -> {target}")
    assert not broken, "broken skill references:\n" + "\n".join(broken)


def test_new_skills_are_registered_in_agents_md():
    agents = AGENTS_MD.read_text(encoding="utf-8")
    for name in ("web2-exposure", "dorking-osint"):
        assert f"`skills/{name}/`" in agents, f"{name} is not listed in AGENTS.md"
        assert (SKILLS_DIR / name / "SKILL.md").is_file()


def test_reference_directories_only_contain_markdown():
    for ref_dir in SKILLS_DIR.glob("*/references"):
        for item in ref_dir.iterdir():
            assert item.is_file(), f"unexpected directory in {ref_dir}: {item.name}"
            assert item.suffix == ".md", f"unexpected file in {ref_dir}: {item.name}"


def test_no_skill_is_empty_or_frontmatter_only():
    for path in skill_files():
        body = _FRONTMATTER_RE.sub("", path.read_text(encoding="utf-8"), count=1).strip()
        assert len(body) >= 200, f"{path}: body too short ({len(body)} chars)"