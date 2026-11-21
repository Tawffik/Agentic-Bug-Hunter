#!/usr/bin/env python3
"""Validate and ingest a BugBountyCI `agent-handoff/` directory.

Contract: `schemas/lifecycle.schema.json`.

Directory layout:
  target_profile.json  assets.jsonl  leads.jsonl  evidence.json  run_meta.json

The tool validates required fields, dedupes leads, ranks them, and optionally
adds them to the local lead board so a hunt does not lose recon leads.

Usage:
  python3 bughunter/tools/handoff_ingest.py path/to/agent-handoff
  python3 bughunter/tools/handoff_ingest.py path/to/agent-handoff --ingest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


@dataclass
class Lead:
    id: str
    cls: str
    title: str
    severity: str
    confidence: str
    status: str
    source: str
    evidence_ref: str
    dedupe_key: str
    next_action: str


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _require(obj: dict, fields: tuple[str, ...], where: str) -> None:
    missing = [f for f in fields if f not in obj or obj[f] is None or obj[f] == ""]
    if missing:
        raise ValueError(f"{where}: missing required field(s): {', '.join(missing)}")


def validate(handoff: dict) -> None:
    _require(handoff, ("target_profile", "assets", "leads", "evidence", "run_meta"), "handoff")
    profile = handoff["target_profile"]
    _require(profile, ("target", "scope", "platform", "program", "technologies"), "target_profile")
    if not isinstance(profile["scope"], list):
        raise ValueError("target_profile.scope must be a list")
    meta = handoff["run_meta"]
    _require(meta, ("run_id", "target", "producer", "generated_at"), "run_meta")
    for i, lead in enumerate(handoff["leads"]):
        _require(lead, ("id", "class", "severity", "confidence", "status", "source", "dedupe_key"),
                 f"leads[{i}]")


def normalize_leads(raw: list[dict]) -> list[Lead]:
    out: dict[str, Lead] = {}
    for row in raw:
        key = row.get("dedupe_key") or row.get("id") or hashlib.sha256(
            json.dumps(row, sort_keys=True).encode()).hexdigest()[:16]
        lead = Lead(
            id=str(row.get("id") or key),
            cls=str(row.get("class") or row.get("type") or "unknown"),
            title=str(row.get("title") or row.get("signal") or row.get("class") or "lead"),
            severity=str(row.get("severity") or "info").lower(),
            confidence=str(row.get("confidence") or "medium").lower(),
            status=str(row.get("status") or "new").lower(),
            source=str(row.get("source") or "bugbountyi"),
            evidence_ref=str(row.get("evidence_ref") or ""),
            dedupe_key=str(key),
            next_action=str(row.get("next_action") or "verify scope and reproduce"),
        )
        if key not in out:
            out[key] = lead
    return sorted(out.values(), key=lambda l: (SEVERITY_RANK.get(l.severity, 9), l.cls, l.id))


def load_handoff(directory: Path) -> dict:
    profile = _read_json(directory / "target_profile.json")
    assets = _read_jsonl(directory / "assets.jsonl")
    leads = _read_jsonl(directory / "leads.jsonl")
    evidence = _read_json(directory / "evidence.json")
    meta = _read_json(directory / "run_meta.json")
    handoff = {
        "schema_version": "1.0",
        "target_profile": profile,
        "assets": assets,
        "leads": leads,
        "evidence": evidence,
        "run_meta": meta,
    }
    validate(handoff)
    return handoff


def ingest_lead_board(target: str, leads: list[Lead]) -> int:
    import lead_board
    added = 0
    for lead in leads:
        try:
            lead_board.add(
                target,
                skill=f"hunt-{lead.cls}" if not lead.cls.startswith("hunt-") else lead.cls,
                evidence=lead.evidence_ref or lead.title,
                signal=lead.title,
                priority="high" if lead.severity in {"critical", "high"} else "med",
                finding_id=lead.id,
            )
            added += 1
        except Exception as exc:
            print(f"[!] lead {lead.id}: {exc}", file=sys.stderr)
    return added


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate/ingest a BugBountyCI lifecycle handoff.")
    parser.add_argument("handoff", help="agent-handoff directory")
    parser.add_argument("--ingest", action="store_true", help="Add leads to lead_board")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    directory = Path(args.handoff)
    try:
        handoff = load_handoff(directory)
    except Exception as exc:
        print(f"invalid handoff: {exc}", file=sys.stderr)
        return 1

    leads = normalize_leads(handoff["leads"])
    profile = handoff["target_profile"]
    summary = {
        "target": profile["target"],
        "platform": profile.get("platform", ""),
        "program": profile.get("program", ""),
        "assets": len(handoff["assets"]),
        "leads": len(leads),
        "evidence": len(handoff["evidence"]),
        "run_id": handoff["run_meta"]["run_id"],
        "top": [asdict(l) for l in leads[:10]],
    }
    if args.ingest:
        summary["ingested"] = ingest_lead_board(profile["target"], leads)

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"target:      {summary['target']} ({summary['platform']}:{summary['program']})")
    print(f"run:         {summary['run_id']}")
    print(f"assets:      {summary['assets']}")
    print(f"leads:       {summary['leads']}")
    print(f"evidence:    {summary['evidence']}")
    if args.ingest:
        print(f"ingested:    {summary['ingested']}")
    print("\nTop leads:")
    for lead in leads[:10]:
        print(f"  [{lead.severity}/{lead.confidence}] {lead.cls} — {lead.title} ({lead.id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
