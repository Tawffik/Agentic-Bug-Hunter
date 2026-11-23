#!/usr/bin/env python3
"""Process metrics — measure the evidence chain, not just the flag count.

ATOBench showed a solved task can hide a fabricated evidence chain; a benchmark
of "confirmed vs not" rewards exactly the wrong behavior. This scores a batch of
validation records on process quality:

  grounded_verification_rate  report_ready / technically_confirmed
  contract_pass_rate          contract satisfied / contract required
  falsification_rate          adversarial FALSIFIED / adversarial run
  false_positive_suppressed   confirmed but correctly held back

Plus stage partial credit for partial-credit scoring (PentestEval/DeepRed).

    python3 -m tools.process_metrics --validation-dir findings/acme.com --json
"""
from __future__ import annotations

import argparse
import glob
import json
import os


def _is_report_ready(v: dict) -> bool:
    try:
        from tools.validate_core import is_report_ready
        return bool(is_report_ready(v))
    except Exception:  # noqa: BLE001
        return v.get("status") == "validated_finding" and bool(
            (v.get("verifier") or {}).get("confirmed"))


def _rate(num: int, den: int) -> float:
    return round(num / den, 4) if den else 0.0


def score(validations: list[dict]) -> dict:
    total = len(validations)
    technically = sum(1 for v in validations if v.get("technically_confirmed"))
    ready = sum(1 for v in validations if _is_report_ready(v))
    skipped = sum(1 for v in validations if (v.get("verifier") or {}).get("skipped"))

    adv = [v.get("adversarial") for v in validations if v.get("adversarial")]
    falsified = sum(1 for a in adv if a.get("verdict") == "FALSIFIED")
    survives = sum(1 for a in adv if a.get("verdict") == "SURVIVES")
    inconclusive = sum(1 for a in adv if a.get("verdict") == "INCONCLUSIVE")

    required = sum(1 for v in validations if v.get("contract_required"))
    satisfied = sum(1 for v in validations if v.get("contract_required")
                    and v.get("contract_satisfied"))

    suppressed = sum(1 for v in validations
                     if v.get("technically_confirmed") and not _is_report_ready(v))

    return {
        "schema": "process-metrics/1",
        "total": total,
        "technically_confirmed": technically,
        "report_ready": ready,
        "verifier_skipped": skipped,
        "grounded_verification_rate": _rate(ready, technically),
        "contract_required": required,
        "contract_satisfied": satisfied,
        "contract_pass_rate": _rate(satisfied, required),
        "adversarial_runs": len(adv),
        "falsified": falsified,
        "survives": survives,
        "inconclusive": inconclusive,
        "falsification_rate": _rate(falsified, len(adv)),
        "false_positive_suppressed": suppressed,
    }


def stage_credit(done: dict[str, bool], weights: dict[str, float] | None = None) -> dict:
    """Weighted partial credit across pipeline stages (PentestEval-style)."""
    done = done or {}
    weights = weights or {k: 1.0 for k in done}
    total_w = sum(weights.get(k, 1.0) for k in done) or 1.0
    earned = sum(weights.get(k, 1.0) for k, ok in done.items() if ok)
    return {
        "schema": "stage-credit/1",
        "stages": done,
        "credit": round(earned / total_w, 4),
        "completed": sum(1 for ok in done.values() if ok),
        "total": len(done),
    }


def from_dir(path: str) -> dict:
    files = glob.glob(os.path.join(path, "**", "validation.json"), recursive=True)
    validations = []
    for f in files:
        try:
            validations.append(json.loads(open(f, encoding="utf-8").read()))
        except (OSError, ValueError):
            continue
    out = score(validations)
    out["source"] = path
    out["files"] = len(files)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Evidence-chain / process metrics")
    ap.add_argument("--validation-dir", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    out = from_dir(args.validation_dir)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"grounded_verification_rate : {out['grounded_verification_rate']}")
        print(f"contract_pass_rate         : {out['contract_pass_rate']}")
        print(f"falsification_rate         : {out['falsification_rate']}")
        print(f"report_ready / confirmed   : {out['report_ready']} / {out['technically_confirmed']}")
        print(f"false_positive_suppressed  : {out['false_positive_suppressed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
