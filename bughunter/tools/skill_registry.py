#!/usr/bin/env python3
"""Skill registry — the knowledge lifecycle layer.

The skills are the agent's *procedures*; the lead router says which one to load.
Nothing, however, loaded the corpus at runtime or answered the quality questions
that matter:

  * Is every routing label (`hunt-*`) covered by a real skill? (knowledge gap)
  * Which skills are never routed to, i.e. dead knowledge? (over/under-coverage)
  * What is the cheap, routable summary of each skill? (progressive disclosure /
    RAG seed — Trail of Bits' metadata -> SKILL.md -> references pattern)
  * Are a skill's declared references present on disk? (lifecycle integrity)

This module is that layer. It is deterministic and offline: it reads
`skills/<name>/SKILL.md` frontmatter (+ optional lifecycle fields) and the
`references/` tree, and exposes `load_registry()`, `coverage()`, `index()`,
`audit()`. `coverage()` reuses `lead_board.HUNT_SKILL_MAP` as the single source
of truth for label->skill, so the router and the corpus can never silently drift.

Usage:
  python3 -m tools.skill_registry index      [--json]   # name+description seed
  python3 -m tools.skill_registry coverage   [--json]   # label -> skill map + gaps
  python3 -m tools.skill_registry audit      [--json]   # lifecycle integrity
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools import lead_board  # noqa: E402

REPO_ROOT = os.path.dirname(_REPO)
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

# Optional lifecycle fields a skill may declare; absent is fine.
_LIFECYCLE_FIELDS = ("status", "provenance", "benchmark", "tags", "load_when")
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Tolerant YAML-ish frontmatter parser (no dependency).

    Handles block scalars (``>``/``|``) the same way the harness does, so a
    multi-line description is read whole.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    data: dict = {}
    lines = m.group(1).splitlines()
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
            block = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            value = " ".join(p for p in block if p)
        data[key] = value
    return data


def _references(skill_dir: str) -> list[str]:
    out = []
    ref_root = os.path.join(skill_dir, "references")
    if os.path.isdir(ref_root):
        for root, _dirs, files in os.walk(ref_root):
            for f in files:
                if f.endswith(".md"):
                    out.append(os.path.relpath(os.path.join(root, f), skill_dir))
    return sorted(out)


def load_registry(skills_dir: str = SKILLS_DIR) -> dict[str, dict]:
    """name -> {name, description, path, references, <lifecycle fields>}."""
    reg: dict[str, dict] = {}
    if not os.path.isdir(skills_dir):
        return reg
    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        try:
            text = open(skill_md, errors="replace").read()
        except OSError:
            continue
        meta = parse_frontmatter(text)
        entry = {
            "name": meta.get("name") or name,
            "declared_name": meta.get("name") or "",
            "description": meta.get("description") or "",
            "path": os.path.relpath(skill_md, REPO_ROOT),
            "references": _references(os.path.join(skills_dir, name)),
        }
        for f in _LIFECYCLE_FIELDS:
            if meta.get(f):
                entry[f] = meta[f]
        reg[name] = entry
    return reg


def coverage(registry: dict[str, dict] | None = None) -> dict:
    """Routing-label -> covering skills, plus knowledge gaps and dead knowledge."""
    registry = registry if registry is not None else load_registry()
    known = set(registry)

    labels = {}
    for label, targets in sorted(lead_board.HUNT_SKILL_MAP.items()):
        present = [t for t in targets if t in known]
        missing = [t for t in targets if t not in known]
        labels[label] = {"skills": targets, "present": present, "missing": missing}

    dangling = sorted({t for v in labels.values() for t in v["missing"]})
    routed = {t for v in labels.values() for t in v["present"]}
    unrouted = sorted(known - routed)

    return {
        "schema": "skill-coverage/1",
        "skills": len(known),
        "labels": len(labels),
        "labels_map": labels,
        "dangling_targets": dangling,      # knowledge gap: label -> missing skill
        "skills_never_routed": unrouted,   # over-coverage: knowledge nothing routes to
    }


def index(registry: dict[str, dict] | None = None) -> list[dict]:
    """Cheap routable summary (progressive disclosure / RAG seed)."""
    registry = registry if registry is not None else load_registry()
    return [{"name": e["name"], "description": e["description"][:280],
             "references": len(e["references"])} for e in
            (registry[k] for k in sorted(registry))]


def audit(registry: dict[str, dict] | None = None) -> list[dict]:
    """Lifecycle integrity issues (deterministic)."""
    registry = registry if registry is not None else load_registry()
    issues = []
    for name, e in registry.items():
        if not e["declared_name"]:
            issues.append({"skill": name, "issue": "missing-frontmatter-name"})
        elif e["declared_name"] != name:
            issues.append({"skill": name, "issue": f"name!=dir ({e['declared_name']})"})
        if len(e["description"]) < 40:
            issues.append({"skill": name, "issue": "description-too-short"})
        for ref in e["references"]:
            if not os.path.isfile(os.path.join(REPO_ROOT, "skills", name, ref)):
                issues.append({"skill": name, "issue": f"missing-reference {ref}"})
    return issues


_HEADING_RE = re.compile(r"^##\s+(.+)$", re.M)


def _headings(text: str) -> set[str]:
    return {h.strip().lower() for h in _HEADING_RE.findall(text)}


def _metrics(name: str, e: dict) -> dict:
    try:
        text = open(os.path.join(REPO_ROOT, e["path"]), errors="replace").read()
    except OSError:
        text = ""
    low = text.lower()
    return {
        "skill": name,
        "lines": text.count("\n"),
        "references": len(e["references"]),
        "sections": len(_HEADING_RE.findall(text)),
        "code_blocks": text.count("```") // 2,
        "has_kill_checklist": bool(re.search(r"kill checklist|kill signal|never.submit", low)),
        "has_routing_table": bool(re.search(r"routing|signal.*->.*move|signal.*run", low)),
        "has_evidence_rule": bool(re.search(r"confirmed|not executed|evidence", low)),
    }


def quality(registry: dict[str, dict] | None = None, overlap_threshold: float = 0.5) -> dict:
    """Quality scorecard: per-skill shape + near-duplicate (overlap) detection.

    Overlap is heading-Jaccard between skills — a high value means two skills
    teach largely the same outline (redundant/divergent guidance risk).
    """
    registry = registry if registry is not None else load_registry()
    metrics = [_metrics(n, registry[n]) for n in sorted(registry)]

    heads = {}
    for n in registry:
        try:
            heads[n] = _headings(open(os.path.join(REPO_ROOT, registry[n]["path"]),
                                      errors="replace").read())
        except OSError:
            heads[n] = set()
    names = sorted(heads)
    overlaps = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ha, hb = heads[a], heads[b]
            if not ha or not hb:
                continue
            j = len(ha & hb) / len(ha | hb)
            if j >= overlap_threshold:
                overlaps.append({"a": a, "b": b, "jaccard": round(j, 2),
                                 "shared_headings": sorted(ha & hb)[:8]})
    overlaps.sort(key=lambda x: -x["jaccard"])

    thin = [m["skill"] for m in metrics if m["sections"] < 5]
    no_refs = [m["skill"] for m in metrics if m["references"] == 0]
    return {
        "schema": "skill-quality/1",
        "skills": len(metrics),
        "metrics": metrics,
        "overlaps": overlaps,
        "thin_no_structure": thin,
        "no_references": no_refs,
    }


def recommendations(registry: dict[str, dict] | None = None) -> list[dict]:
    """Structural quality advisories (not errors) — what to polish per skill."""
    registry = registry if registry is not None else load_registry()
    recs = []
    for name in sorted(registry):
        m = _metrics(name, registry[name])
        r = []
        if not m["has_routing_table"]:
            r.append("no-routing-table")
        if not m["has_kill_checklist"]:
            r.append("no-kill-checklist")
        if m["references"] == 0 and m["lines"] > 600:
            r.append("large-skill-no-references")  # split detail into references/
        if r:
            recs.append({"skill": name, "recommend": r})
    return recs


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Skill registry / knowledge coverage")
    p.add_argument("cmd", choices=["index", "coverage", "audit", "quality", "recommend"])
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.cmd == "index":
        data = index()
    elif args.cmd == "coverage":
        data = coverage()
    elif args.cmd == "quality":
        data = quality()
    elif args.cmd == "recommend":
        data = recommendations()
    else:
        data = audit()

    if args.json:
        print(json.dumps(data, indent=2))
    elif args.cmd == "coverage":
        cov = data
        print(f"skills: {cov['skills']} | routing labels: {cov['labels']}")
        print(f"dangling label targets (knowledge gaps): {cov['dangling_targets'] or 'none'}")
        print(f"skills never routed to (dead knowledge): {cov['skills_never_routed'] or 'none'}")
    elif args.cmd == "quality":
        q = data
        print(f"skills: {q['skills']} | no references: {len(q['no_references'])} | "
              f"thin/no-structure: {len(q['thin_no_structure'])}")
        print(f"near-duplicate skill pairs (jaccard>=0.5): {len(q['overlaps'])}")
        for o in q["overlaps"]:
            print(f"  {o['jaccard']}  {o['a']} ~ {o['b']}   shared: {o['shared_headings'][:4]}")
    elif args.cmd == "audit":
        print(f"lifecycle issues: {len(data)}")
        for i in data:
            print(f"  [{i['skill']}] {i['issue']}")
    elif args.cmd == "recommend":
        print(f"structural advisories: {len(data)} skill(s)")
        for r in data:
            print(f"  [{r['skill']}] {', '.join(r['recommend'])}")
    else:
        for e in data:
            print(f"{e['name']:24} ({e['references']} refs)  {e['description'][:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
