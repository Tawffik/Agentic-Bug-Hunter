"""Exploration/asset ledger — persistent per-target coverage memory.

Lightweight port of the ARTEX dual-graph idea (asset store + exploration
"cold graph" with covered-stamps), reviewed in source 2026-11-26
(db/assets.go, db/digest.go). Purpose: a hunt never re-derives recon it
already did. Assets are upserted once per (kind, value); coverage stamps
mark what has been tested, by which run; planners ask `uncovered()` instead
of starting from scratch.

Storage: one JSONL file per target under hunt-memory/exploration/<target>/
(same layout convention as tools/planning_ledger.py). Stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone

_KINDS = {"domain", "subdomain", "ip", "port", "endpoint", "app", "service", "param", "note"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _root(target: str, directory: str | None = None) -> str:
    if directory:
        return directory
    base = os.environ.get("BBHUNT_PLANNING_DIR") or os.path.join(
        os.getcwd(), "hunt-memory", "exploration")
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", target or "unknown")
    return os.path.join(base, safe)


def _path(target: str, directory: str | None = None) -> str:
    return os.path.join(_root(target, directory), "assets.jsonl")


def _aid(kind: str, value: str) -> str:
    norm = " ".join(value.lower().split())
    return hashlib.sha1(f"{kind}|{norm}".encode()).hexdigest()[:12]


def load(target: str, directory: str | None = None) -> dict[str, dict]:
    """Return {asset_id: record}. Later lines win (append-only log)."""
    out: dict[str, dict] = {}
    p = _path(target, directory)
    if not os.path.exists(p):
        return out
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            out[rec["id"]] = rec
    return out


def _append(target: str, rec: dict, directory: str | None = None) -> None:
    p = _path(target, directory)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def upsert_asset(target: str, kind: str, value: str, *, source: str = "",
                 directory: str | None = None) -> str:
    """Insert or refresh one asset. Returns its stable id."""
    if kind not in _KINDS:
        raise ValueError(f"unknown asset kind: {kind!r} (expected one of {sorted(_KINDS)})")
    existing = load(target, directory)
    aid = _aid(kind, value)
    rec = existing.get(aid, {})
    rec.update({
        "id": aid, "kind": kind, "value": value,
        "first_seen": rec.get("first_seen", _now()),
        "last_seen": _now(), "source": source or rec.get("source", ""),
        "covered": rec.get("covered", {}),
    })
    _append(target, rec, directory)
    return aid


def mark_covered(target: str, asset_id: str, *, run: str, note: str = "",
                 directory: str | None = None) -> None:
    """Stamp an asset as tested by a run (the 'cold graph' mark)."""
    existing = load(target, directory)
    rec = existing.get(asset_id)
    if rec is None:
        raise KeyError(f"unknown asset id: {asset_id}")
    cov = rec.setdefault("covered", {})
    cov[run] = {"at": _now(), "note": note}
    _append(target, rec, directory)


def uncovered(target: str, kind: str | None = None, directory: str | None = None) -> list[dict]:
    """Assets with no coverage stamp — what a planner should work on next."""
    return [r for r in load(target, directory).values()
            if not r.get("covered") and (kind is None or r["kind"] == kind)]


def summary(target: str, directory: str | None = None) -> dict:
    assets = load(target, directory)
    cov = sum(1 for r in assets.values() if r.get("covered"))
    by_kind: dict[str, int] = {}
    for r in assets.values():
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
    return {"target": target, "assets": len(assets), "covered": cov,
            "uncovered": len(assets) - cov, "by_kind": by_kind}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Exploration/asset ledger")
    ap.add_argument("target")
    ap.add_argument("--add", nargs=2, metavar=("KIND", "VALUE"))
    ap.add_argument("--source", default="cli")
    ap.add_argument("--cover", metavar="ASSET_ID")
    ap.add_argument("--run", default="manual")
    ap.add_argument("--uncovered", action="store_true")
    args = ap.parse_args(argv)
    if args.add:
        print(upsert_asset(args.target, args.add[0], args.add[1], source=args.source))
    if args.cover:
        mark_covered(args.target, args.cover, run=args.run)
    if args.uncovered:
        for r in uncovered(args.target):
            print(f'{r["id"]}  {r["kind"]:9s}  {r["value"]}')
    print(json.dumps(summary(args.target), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
