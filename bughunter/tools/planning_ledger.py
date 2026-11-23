#!/usr/bin/env python3
"""Planning ledger — hold a hypothesis until it is converted or killed.

The 2026 finding (Big Enough to Break Out) is counter-intuitive: adding a
coverage-memory layer did NOT help agents — the limiter was **planning and
commitment**. Agents held evidence for a route and never turned it into an
exploitation hypothesis. This ledger makes that commitment explicit and durable:

    held        an open hypothesis worth pursuing
    converted   turned into a validated finding (link it)
    killed      disproven / out of scope / not worth it — with a reason

It is deliberately separate from the lead board: the board tracks *recon
signals*, the ledger tracks *hunter intent* (what you mean to prove next).

    python3 -m tools.planning_ledger add --target acme.com \
        --hypothesis "order id is sequential and unowned" --vuln-class idor
    python3 -m tools.planning_ledger next --target acme.com
    python3 -m tools.planning_ledger touch --target acme.com --id H-1a2b --status converted
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
from datetime import datetime, timezone

SCHEMA = "planning/1"
STATUSES = ("held", "converted", "killed")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _root(target: str, directory: str | None = None) -> str:
    if directory:
        return directory
    base = os.environ.get("BBHUNT_PLANNING_DIR") or os.path.join(
        os.getcwd(), "hunt-memory", "planning")
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", target or "unknown")
    return os.path.join(base, safe)


def ledger_path(target: str, directory: str | None = None) -> str:
    return os.path.join(_root(target, directory), "hypotheses.jsonl")


def _hash(target: str, hypothesis: str) -> str:
    norm = " ".join(hypothesis.lower().split())
    return hashlib.sha1(f"{target}|{norm}".encode()).hexdigest()[:10]


@contextlib.contextmanager
def _lock(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lock_path = path + ".lock"
    with open(lock_path, "a+", encoding="utf-8") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def load(target: str, directory: str | None = None) -> list[dict]:
    path = ledger_path(target, directory)
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8", errors="ignore"):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
    return out


def add(target: str, hypothesis: str, *, vuln_class: str = "", endpoint: str = "",
        confidence: str = "medium", evidence: list[str] | None = None,
        chain_to: list[str] | None = None, directory: str | None = None) -> dict:
    hypothesis = (hypothesis or "").strip()
    if not hypothesis:
        raise ValueError("hypothesis must not be empty")
    hid = f"H-{_hash(target, hypothesis)}"
    path = ledger_path(target, directory)
    with _lock(path):
        existing = {r.get("id"): r for r in load(target, directory)}
        if hid in existing and existing[hid].get("status") == "held":
            return existing[hid]
        rec = {
            "schema": SCHEMA,
            "id": hid,
            "target": target,
            "hypothesis": hypothesis,
            "vuln_class": vuln_class,
            "endpoint": endpoint,
            "confidence": confidence,
            "status": "held",
            "evidence": evidence or [],
            "chain_to": chain_to or [],
            "created": _now(),
            "updated": _now(),
            "note": "",
        }
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def touch(target: str, hid: str, status: str, note: str = "",
          directory: str | None = None) -> dict | None:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    path = ledger_path(target, directory)
    with _lock(path):
        records = load(target, directory)
        updated = None
        for r in records:
            if r.get("id") == hid:
                r["status"] = status
                r["updated"] = _now()
                if note:
                    r["note"] = note
                updated = r
        if updated is None:
            return None
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
        os.replace(tmp, path)
        return updated


def list_open(target: str, directory: str | None = None) -> list[dict]:
    return [r for r in load(target, directory) if r.get("status") == "held"]


def next_for(target: str, directory: str | None = None) -> dict | None:
    order = {"high": 0, "medium": 1, "low": 2}
    open_items = sorted(list_open(target, directory),
                        key=lambda r: order.get(r.get("confidence", "medium"), 1))
    return open_items[0] if open_items else None


def stale(hours: int = 24, target: str = "", directory: str | None = None) -> list[dict]:
    now = datetime.now(timezone.utc)
    out = []
    for r in load(target, directory):
        if r.get("status") != "held":
            continue
        try:
            ts = datetime.fromisoformat(r.get("updated", r.get("created")))
        except ValueError:
            continue
        if (now - ts).total_seconds() >= hours * 3600:
            out.append(r)
    return out


def summary(target: str, directory: str | None = None) -> dict:
    records = load(target, directory)
    counts = {s: 0 for s in STATUSES}
    for r in records:
        counts[r.get("status", "held")] = counts.get(r.get("status", "held"), 0) + 1
    return {"target": target, "total": len(records), "counts": counts,
            "open": counts.get("held", 0)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Planning / commitment ledger")
    ap.add_argument("--dir", default=None, help="override ledger directory")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--target", required=True)
    a.add_argument("--hypothesis", required=True)
    a.add_argument("--vuln-class", default="")
    a.add_argument("--endpoint", default="")
    a.add_argument("--confidence", default="medium", choices=["high", "medium", "low"])

    t = sub.add_parser("touch")
    t.add_argument("--target", required=True)
    t.add_argument("--id", required=True)
    t.add_argument("--status", required=True, choices=list(STATUSES))
    t.add_argument("--note", default="")

    l = sub.add_parser("list")
    l.add_argument("--target", required=True)
    l.add_argument("--all", action="store_true")

    n = sub.add_parser("next")
    n.add_argument("--target", required=True)

    s = sub.add_parser("summary")
    s.add_argument("--target", required=True)

    args = ap.parse_args(argv)
    if args.cmd == "add":
        rec = add(args.target, args.hypothesis, vuln_class=args.vuln_class,
                  endpoint=args.endpoint, confidence=args.confidence, directory=args.dir)
        print(json.dumps(rec, indent=2))
    elif args.cmd == "touch":
        rec = touch(args.target, args.id, args.status, args.note, directory=args.dir)
        print(json.dumps(rec, indent=2) if rec else "[-] no such hypothesis")
        return 0 if rec else 1
    elif args.cmd == "list":
        recs = load(args.target, args.dir) if args.all else list_open(args.target, args.dir)
        for r in recs:
            print(f"{r['id']}  [{r['status']}/{r.get('confidence')}]  {r['hypothesis']}")
    elif args.cmd == "next":
        rec = next_for(args.target, args.dir)
        print(json.dumps(rec, indent=2) if rec else "[+] no open hypotheses")
    elif args.cmd == "summary":
        print(json.dumps(summary(args.target, args.dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
