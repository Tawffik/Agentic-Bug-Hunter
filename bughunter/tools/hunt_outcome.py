#!/usr/bin/env python3
"""Hunt outcome — answer "why did this hunt produce few/zero findings?".

Recon on a hardened target routinely ends at *0 validated findings*, and the
agent then has no honest way to say **why** — so the next session repeats the
same dead end. This tool reads only local artifacts (the lead board, the
per-target validation records, and any report drafts) and classifies the run
into one of a small set of root causes with a ranked next action.

It is deliberately read-only and network-free: it explains the outcome, it does
not attempt to change it. Deterministic, so it is safe to run at the end of every
session and cheap enough to run on a timer.

Root causes (highest-priority first):
  report_ready_unsubmitted   a validated, report-ready finding exists but no
                             report draft was written — the single biggest miss
  unattempted_leads          leads are still `new`; the hunt loop never ran them
  auth_blocked               leads parked / stalled because a session is needed
  capability_gap             leads parked for lack of a deterministic verifier
  chain_required             an oracle fired but a chain is needed before report
  hardened                   leads were tested and killed — no soft surface

Usage:
    python3 -m tools.hunt_outcome <target> [--leads-dir DIR]
        [--findings-dir DIR ...] [--json]

Exit codes: 0 = a report-ready or progress outcome, 3 = zero findings (so a
caller can branch on it), 2 = no local data for the target.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools import lead_board  # noqa: E402

# Buckets a parked/stalled lead reason can fall into. Keyword match on the
# free-text `note`/reason written by the swarm and verifier gate.
_AUTH_RE = re.compile(
    r"auth|session|permission|login|log\s*in|unauthor|not logged|401|403|"
    r"identity|credential|manual input|token",
    re.I,
)
_NO_VERIFIER_RE = re.compile(r"no (deterministic )?verifier|no verifier for", re.I)
_CHAIN_RE = re.compile(r"chain", re.I)

# A validation record is report-ready when the core gate says so. Import the one
# authoritative implementation rather than re-deriving it (avoids drift).
_REPORT_ARTIFACT_GLOBS = (
    "**/hackerone-report.md",
    "**/bugcrowd-report.md",
    "**/report.md",
    "**/*-report.md",
    "**/submission-notes.md",
)


def _is_report_ready(validation: dict) -> bool:
    try:
        from tools.validate_core import is_report_ready

        return bool(is_report_ready(validation))
    except Exception:  # noqa: BLE001 - fall back to the documented shape
        return validation.get("status") == "validated_finding" and bool(
            (validation.get("verifier") or {}).get("confirmed")
        )


def classify_reason(reason: str) -> str:
    """Bucket a free-text parked/killed reason. Pure function (unit-tested).

    Order matters: a note can mention both a chain and auth; auth is the more
    actionable blocker, so it wins.
    """
    r = reason or ""
    if _AUTH_RE.search(r):
        return "auth"
    if _NO_VERIFIER_RE.search(r):
        return "no_verifier"
    if _CHAIN_RE.search(r):
        return "chain"
    return "other"


def _load_validations(findings_dirs: list[str], target: str) -> list[dict]:
    out: list[dict] = []
    for base in findings_dirs:
        root = os.path.join(base, target)
        for path in glob.glob(os.path.join(root, "**", "validation.json"), recursive=True):
            try:
                with open(path, errors="replace") as fh:
                    data = json.load(fh)
            except (OSError, ValueError):
                continue
            if isinstance(data, dict):
                data["_path"] = path
                out.append(data)
    return out


def _has_report_draft(findings_dirs: list[str], target: str) -> bool:
    for base in findings_dirs:
        root = os.path.join(base, target)
        for pat in _REPORT_ARTIFACT_GLOBS:
            if glob.glob(os.path.join(root, pat), recursive=True):
                return True
    return False


def _counts(leads: list[dict]) -> dict:
    c = {"new": 0, "investigating": 0, "killed": 0, "parked": 0, "reported": 0}
    for ld in leads:
        s = ld.get("status") or "new"
        c[s] = c.get(s, 0) + 1
    return c


def _parked_buckets(leads: list[dict]) -> dict:
    b = {"auth": 0, "no_verifier": 0, "chain": 0, "other": 0}
    for ld in leads:
        if ld.get("status") not in ("parked", "investigating"):
            continue
        bucket = classify_reason(str(ld.get("note", "")))
        b[bucket] = b.get(bucket, 0) + 1
    return b


def analyze(target: str, *, leads: list[dict] | None = None,
            findings_dirs: list[str] | None = None) -> dict:
    """Classify a target's outcome. Pure given its inputs (unit-tested)."""
    if leads is None:
        leads = lead_board.load_ledger(target)
    if findings_dirs is None:
        findings_dirs = [os.path.join(_REPO, "..", "findings"), os.path.join(_REPO, "findings")]
        findings_dirs = [os.path.normpath(d) for d in findings_dirs]

    counts = _counts(leads)
    parked = _parked_buckets(leads)
    validations = _load_validations(findings_dirs, target)
    ready = [v for v in validations if _is_report_ready(v)]
    report_draft = _has_report_draft(findings_dirs, target)

    causes: list[dict] = []
    actions: list[str] = []

    if ready and not report_draft:
        causes.append({
            "code": "report_ready_unsubmitted", "severity": "critical",
            "count": len(ready),
            "detail": f"{len(ready)} report-ready finding(s) with no report draft written",
        })
        actions.append(
            "Run /report for each report-ready finding, then submit — this is a done bug"
        )

    if counts["new"] > 0:
        causes.append({
            "code": "unattempted_leads", "severity": "high", "count": counts["new"],
            "detail": f"{counts['new']} lead(s) still `new` — the hunt loop never ran them",
        })
        actions.append(
            "Run the swarm over the board: "
            f"python3 -m tools.swarm {target} --ingest --workers 6"
        )

    if parked["auth"] > 0:
        causes.append({
            "code": "auth_blocked", "severity": "high", "count": parked["auth"],
            "detail": f"{parked['auth']} lead(s) stalled on an authenticated session",
        })
        actions.append(
            "Supply an auth session (--auth-file/--cookie) and, for IDOR, two "
            "identities via /authz-diff — most paying bugs sit behind login"
        )

    if parked["no_verifier"] > 0:
        causes.append({
            "code": "capability_gap", "severity": "medium", "count": parked["no_verifier"],
            "detail": f"{parked['no_verifier']} lead(s) parked with no deterministic verifier",
        })
        actions.append(
            "Route these leads to an AI-assisted hunt skill, or add a verifier "
            "under tools/verifiers/ if the class is recurring"
        )

    if parked["chain"] > 0:
        causes.append({
            "code": "chain_required", "severity": "medium", "count": parked["chain"],
            "detail": f"{parked['chain']} oracle-confirmed lead(s) held for a chain",
        })
        actions.append("Run /chain on the oracle-confirmed leads to reach reportable impact")

    if counts["killed"] > 0 and counts["new"] == 0 and not ready:
        causes.append({
            "code": "hardened", "severity": "info", "count": counts["killed"],
            "detail": f"{counts['killed']} lead(s) tested and killed — surface is hardened",
        })
        actions.append(
            "Pivot: deepen recon (more hosts/params), mine JS for hidden APIs, "
            "or move to a lower-duplicate asset in scope"
        )

    if ready and report_draft:
        causes.append({
            "code": "report_drafted", "severity": "info", "count": len(ready),
            "detail": f"{len(ready)} report-ready finding(s); a report draft exists",
        })

    has_data = bool(leads or validations or report_draft)
    if not has_data:
        verdict = "no_data"
    elif report_draft and not ready and not counts["new"]:
        verdict = "report_drafted"
    elif ready and not report_draft:
        verdict = "report_ready_unsubmitted"
    elif counts["new"] > 0:
        verdict = "unattempted_leads"
    elif parked["auth"] > 0:
        verdict = "auth_blocked"
    elif parked["no_verifier"] > 0:
        verdict = "capability_gap"
    elif parked["chain"] > 0:
        verdict = "chain_required"
    elif counts["killed"] > 0:
        verdict = "hardened"
    else:
        verdict = "progress"

    return {
        "schema": "hunt-outcome/1",
        "target": target,
        "verdict": verdict,
        "counts": counts,
        "parked_buckets": parked,
        "validations": len(validations),
        "report_ready": len(ready),
        "report_draft": report_draft,
        "causes": causes,
        "next_actions": actions,
    }


def render(result: dict) -> str:
    lines = [
        f"HUNT OUTCOME — {result['target']}",
        f"verdict: {result['verdict']}",
        f"leads: {result['counts']}",
        f"validations: {result['validations']} (report-ready: {result['report_ready']}, "
        f"draft: {result['report_draft']})",
        "",
    ]
    if not result["causes"]:
        if result["report_draft"]:
            lines.append("A report draft exists (no local lead board / validation record).")
        else:
            lines.append("No outcome data — has recon/ingest been run for this target?")
        return "\n".join(lines)
    lines.append("Why:")
    for c in result["causes"]:
        lines.append(f"  [{c['severity']:8}] {c['code']}: {c['detail']}")
    if result["next_actions"]:
        lines.append("")
        lines.append("Next:")
        for a in result["next_actions"]:
            lines.append(f"  - {a}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Explain a hunt's outcome (why few/zero findings)")
    p.add_argument("target")
    p.add_argument("--leads-dir", default=None, help="override the lead-board directory")
    p.add_argument("--findings-dir", action="append", default=None,
                   help="findings root to scan (repeatable)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    leads = None
    if args.leads_dir:
        # Read the ledger from an explicit directory (tests / non-default homes).
        path = os.path.join(args.leads_dir,
                            re.sub(r"[^\w.-]", "_", args.target) + ".jsonl")
        leads = []
        if os.path.exists(path):
            with open(path, errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            leads.append(json.loads(line))
                        except ValueError:
                            pass

    result = analyze(args.target, leads=leads, findings_dirs=args.findings_dir)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))

    if result["verdict"] == "no_data":
        return 2
    if result["verdict"] in ("hardened",) and result["report_ready"] == 0:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
