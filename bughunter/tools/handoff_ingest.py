#!/usr/bin/env python3
"""Validate and ingest a BugBountyCI `agent-handoff/` directory.

Contract: `schemas/lifecycle.schema.json`.

Directory layout:
  target_profile.json  assets.jsonl  leads.jsonl  evidence.json  run_meta.json

The tool validates required fields, dedupes leads, ranks them, and optionally
adds them to the local lead board so a hunt does not lose recon leads.

Delta-first: ingested runs and leads are persisted in `memory/handoff-state.json`
so a repeated or overlapping handoff only surfaces new leads. A previously seen
lead that arrives with a changed status updates the existing board lead instead
of creating a duplicate.

Usage:
  python3 bughunter/tools/handoff_ingest.py path/to/agent-handoff
  python3 bughunter/tools/handoff_ingest.py path/to/agent-handoff --ingest
  python3 bughunter/tools/handoff_ingest.py path/to/agent-handoff --ingest --reset-delta
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "memory" / "handoff-state.json"
STATUS_FLOW = {"new", "investigating", "killed", "reported", "parked"}
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


# ---------------------------------------------------------------------------
# Delta state — memory/handoff-state.json
# ---------------------------------------------------------------------------

def state_path(override: str | None = None) -> Path:
    return Path(override) if override else DEFAULT_STATE


def _empty_state() -> dict:
    return {"version": 1, "targets": {}}


def _target_key(target: str) -> str:
    return re.sub(r"[^\w.-]", "_", target.lower())


def load_state(path: Path) -> dict:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return _empty_state()
    if not isinstance(state, dict) or not isinstance(state.get("targets"), dict):
        return _empty_state()
    return state


def target_state(state: dict, target: str) -> dict:
    entry = state["targets"].setdefault(_target_key(target), {"runs": [], "leads": {}})
    entry.setdefault("runs", [])
    entry.setdefault("leads", {})
    return entry


def save_state(path: Path, state: dict) -> None:
    created_dir = not path.parent.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    if created_dir:
        os.chmod(path.parent, 0o700)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    fd = os.open(tmp, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


@contextlib.contextmanager
def state_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path) + ".lock", os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def partition_leads(leads: list[Lead], entry: dict) -> tuple[list[Lead], list[Lead]]:
    """Split ranked leads into unseen leads and already-seen leads."""
    seen = entry["leads"]
    fresh = [l for l in leads if l.dedupe_key not in seen]
    known = [l for l in leads if l.dedupe_key in seen]
    return fresh, known


def ingest_lead_board(target: str, leads: list[Lead], entry: dict,
                      run_id: str) -> tuple[int, int, int]:
    """Add fresh leads, reconcile changed statuses, and record delta state.

    Returns (added, updated, failed). Failed leads stay unmarked so a later run
    retries them.
    """
    import lead_board
    added = updated = failed = 0
    seen = entry["leads"]
    for lead in leads:
        record = seen.get(lead.dedupe_key)
        if record:
            board_id = record.get("board_id")
            status = lead.status if lead.status in STATUS_FLOW else record.get("status", "new")
            if board_id and status != record.get("status"):
                try:
                    lead_board.touch(target, board_id, status, note=f"handoff status ({run_id})")
                    record["status"] = status
                    record["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    updated += 1
                except Exception as exc:
                    print(f"[!] lead {lead.id}: {exc}", file=sys.stderr)
                    failed += 1
            continue
        try:
            evidence = " · ".join(p for p in (lead.evidence_ref, lead.title) if p) or lead.id
            board_lead = lead_board.add(
                target,
                skill=f"hunt-{lead.cls}" if not lead.cls.startswith("hunt-") else lead.cls,
                evidence=evidence,
                signal=lead.title,
                priority="high" if lead.severity in {"critical", "high"} else "med",
                finding_id=lead.id,
            )
            if board_lead is None:
                print(f"[!] lead {lead.id}: rejected by adjudication", file=sys.stderr)
                failed += 1
                continue
            seen[lead.dedupe_key] = {
                "finding_id": lead.id,
                "board_id": board_lead.get("id"),
                "status": lead.status,
                "ingested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            added += 1
        except Exception as exc:
            print(f"[!] lead {lead.id}: {exc}", file=sys.stderr)
            failed += 1
    return added, updated, failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate/ingest a BugBountyCI lifecycle handoff.")
    parser.add_argument("handoff", help="agent-handoff directory")
    parser.add_argument("--ingest", action="store_true", help="Add new leads to lead_board")
    parser.add_argument("--state", default=None, help=f"delta state file (default: {DEFAULT_STATE})")
    parser.add_argument("--reset-delta", action="store_true",
                        help="clear delta state for the handoff target before running")
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
    target = profile["target"]
    run_id = handoff["run_meta"]["run_id"]
    state_file = state_path(args.state)

    if args.reset_delta:
        with state_lock(state_file):
            state = load_state(state_file)
            removed = state["targets"].pop(_target_key(target), None) is not None
            save_state(state_file, state)
        print(("[+] delta state cleared for " if removed else "[.] no delta state for ")
              + f"{target}", file=sys.stderr)

    if args.ingest:
        added = updated = failed = 0
        with state_lock(state_file):
            state = load_state(state_file)
            entry = target_state(state, target)
            already_run = run_id in entry["runs"]
            fresh, known = partition_leads(leads, entry)
            with contextlib.redirect_stdout(sys.stderr):
                added, updated, failed = ingest_lead_board(target, leads, entry, run_id)
            if run_id not in entry["runs"]:
                entry["runs"] = (entry["runs"] + [run_id])[-200:]
            entry["last_seen"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            save_state(state_file, state)
    else:
        added = updated = failed = None
        state = load_state(state_file)
        entry = target_state(state, target)
        already_run = run_id in entry["runs"]
        fresh, known = partition_leads(leads, entry)

    summary = {
        "target": target,
        "platform": profile.get("platform", ""),
        "program": profile.get("program", ""),
        "assets": len(handoff["assets"]),
        "leads": len(leads),
        "new_leads": len(fresh),
        "skipped_seen": len(known),
        "already_ingested_run": already_run,
        "evidence": len(handoff["evidence"]),
        "run_id": run_id,
        "top": [asdict(l) for l in fresh[:10]],
        "ingested": added,
        "updated": updated,
        "failed": failed,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
        return 1 if summary.get("failed") else 0

    print(f"target:      {target} ({summary['platform']}:{summary['program']})")
    print(f"run:         {run_id}" + ("  (already ingested)" if already_run else ""))
    print(f"assets:      {summary['assets']}")
    print(f"leads:       {summary['leads']}  (new: {len(fresh)}, already seen: {len(known)})")
    print(f"evidence:    {summary['evidence']}")
    if args.ingest:
        print(f"ingested:    {added}  (updated: {updated}, failed: {failed})")
    if not fresh:
        print("\nNo new leads — delta is clean.")
        return 1 if summary.get("failed") else 0
    print("\nTop new leads:")
    for lead in fresh[:10]:
        print(f"  [{lead.severity}/{lead.confidence}] {lead.cls} — {lead.title} ({lead.id})")
    return 1 if summary.get("failed") else 0


if __name__ == "__main__":
    raise SystemExit(main())
