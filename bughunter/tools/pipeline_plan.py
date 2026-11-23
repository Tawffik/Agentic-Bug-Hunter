#!/usr/bin/env python3
"""Pipeline plan — turn lead boards into an executable, chunked work plan.

The boards hold the leads; this chunks them into ordered work units so the hunt
can "go deep" on one lane at a time instead of re-reading everything. Lanes map
to the pipeline stage that can actually advance a lead:

  auto   class has a deterministic verifier      -> run the swarm
  authz  idor/bola (needs two identities)        -> /authz-diff
  ai     no verifier, but a skill covers it       -> load that skill (manual/AI)

Chunks are ordered by (target value, priority, lane), size-capped, and each
carries the exact next command. Read-only and offline.

Usage:
  python3 -m tools.pipeline_plan --all                 # every board on disk
  python3 -m tools.pipeline_plan --target tiktok.com   # one target
  python3 -m tools.pipeline_plan --all --json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools import lead_board  # noqa: E402
from tools.verifiers import normalize_class  # noqa: E402

LANE_PRIORITY = {"auto": 0, "authz": 1, "ai": 2}
_PRIO = {"high": 0, "med": 1, "low": 2}
_AUTHZ = {"idor", "bola", "graphql-idor", "mass-assignment"}


def _lane(skill: str) -> str:
    canon = normalize_class(str(skill).replace("hunt-", "").replace("-", " "))
    if canon in _AUTHZ:
        return "authz"
    if canon:
        return "auto"
    return "ai"


def _action(target: str, lane: str, skills: set[str]) -> str:
    if lane == "auto":
        return f"python3 -m tools.swarm {target} --ingest --workers 6"
    if lane == "authz":
        return (f"python3 -m tools.hunt {target} --headers-a A --headers-b B "
                f"--confirm   (or: python3 -m tools.authz_diff ...)")
    mapped = sorted({s for sk in skills for s in lead_board.skills_for(sk)})
    return "load skill(s): " + (", ".join(mapped) if mapped else "?")


def build_plan(leads_by_target: dict[str, list[dict]], chunk_size: int = 10) -> dict:
    """Pure chunker: {target: [leads]} -> ordered chunks."""
    chunks = []
    for target, leads in leads_by_target.items():
        new = [l for l in leads if l.get("status", "new") == "new"]
        if not new:
            continue
        groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for l in new:
            groups[(_lane(l.get("skill", "")), l.get("priority", "low"))].append(l)
        for (lane, prio), items in groups.items():
            items.sort(key=lead_board.rank_key)
            skills = {i.get("skill", "") for i in items}
            for i in range(0, len(items), chunk_size):
                part = items[i:i + chunk_size]
                chunks.append({
                    "target": target,
                    "lane": lane,
                    "priority": prio,
                    "count": len(part),
                    "skills": sorted(skills),
                    "sample": [p.get("evidence", "")[:80] for p in part[:4]],
                    "action": _action(target, lane, skills),
                })
    # order: target with most high-value first, then lane, then priority
    tgt_weight = defaultdict(int)
    for c in chunks:
        tgt_weight[c["target"]] += c["count"] * (3 if c["priority"] == "high" else 1)
    chunks.sort(key=lambda c: (-tgt_weight[c["target"]], LANE_PRIORITY[c["lane"]],
                               _PRIO.get(c["priority"], 3), -c["count"]))
    for n, c in enumerate(chunks, 1):
        c["chunk_id"] = f"chunk-{n:02d}"
    return {"schema": "pipeline-plan/1", "chunks": chunks,
            "totals": {"targets": len({c['target'] for c in chunks}),
                       "chunks": len(chunks),
                       "leads": sum(c["count"] for c in chunks)}}


def leads_on_disk(leads_dir: str | None = None) -> dict[str, list[dict]]:
    d = leads_dir or lead_board.LEADS_DIR
    out = {}
    for path in glob.glob(os.path.join(d, "*.jsonl")):
        target = os.path.basename(path)[:-6]
        out[target] = lead_board.load_ledger(target)
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Chunked pipeline plan from lead boards")
    p.add_argument("--target", action="append", default=[])
    p.add_argument("--all", action="store_true")
    p.add_argument("--chunk-size", type=int, default=10)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    allb = leads_on_disk()
    if args.target:
        boards = {t: allb.get(t, lead_board.load_ledger(t)) for t in args.target}
    elif args.all:
        boards = allb
    else:
        boards = allb
    plan = build_plan(boards, chunk_size=args.chunk_size)

    if args.json:
        print(json.dumps(plan, indent=2))
        return 0
    print(f"PIPELINE PLAN — {plan['totals']['targets']} targets, "
          f"{plan['totals']['chunks']} chunks, {plan['totals']['leads']} untouched leads\n")
    for c in plan["chunks"]:
        print(f"{c['chunk_id']} [{c['lane']:5}/{c['priority']:4}] {c['target']:18} "
              f"x{c['count']}  {','.join(s.replace('hunt-','') for s in c['skills'])[:50]}")
        print(f"     action: {c['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())