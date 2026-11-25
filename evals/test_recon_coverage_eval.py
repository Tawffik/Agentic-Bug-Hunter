"""Eval harness — recon-plan coverage fixture (F3, offline scorer validation).

Validates evals/recon_coverage.py against synthetic plans for lab.example.
The scorer itself is the deliverable reused for real model-produced plans
once a verified free provider exists (phase 0, owner decision pending).
Prints EVAL_RESULT JSON lines like the other eval modules.
"""

import json
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from evals.recon_coverage import REFERENCE_CHECKLIST, score_plan  # noqa: E402


def _emit(fixture, expected, actual, note):
    record = {
        "fixture": fixture,
        "expected": expected,
        "actual": actual,
        "pass": expected == actual,
        "note": note[:140],
    }
    print("EVAL_RESULT " + json.dumps(record, ensure_ascii=False))
    return record


FULL_PLAN = """Recon plan for lab.example:
1. Subdomain enumeration with subfinder and amass.
2. Port scan with nmap for open ports.
3. Technology fingerprinting with whatweb (expect nginx/PHP/WordPress).
4. JavaScript file analysis with linkfinder for hidden routes.
5. Parameter discovery with arjun on all forms and query strings.
6. Enumerate the /api/v1 endpoints; look for swagger/openapi docs.
7. Probe /uploads for file upload weaknesses.
8. WordPress-specific checks: wpscan, wp-json user enumeration, wp-content listing.
9. Auth surface: wp-login brute protection, session cookie flags.
10. Content discovery with ffuf for hidden directories.
"""

PARTIAL_PLAN = """Recon plan for lab.example:
1. Run nmap for open ports.
2. Fingerprint the technology stack.
3. Directory bruteforce with gobuster.
"""

EMPTY_PLAN = "TODO: think about recon later."


def test_f3_full_plan_scores_complete_coverage():
    result = score_plan(FULL_PLAN)
    ok = result["coverage"] == 1.0
    assert ok, f"missed: {result['missed']}"
    _emit("F3-full", True, ok, "complete synthetic plan covers all 10 checklist items")


def test_f3_partial_plan_reports_exact_misses():
    result = score_plan(PARTIAL_PLAN)
    ok = result["covered_count"] == 3 and result["total_count"] == len(REFERENCE_CHECKLIST)
    assert ok, result
    assert "subdomain-enum" in result["missed"]
    assert "wordpress-checks" in result["missed"]
    _emit("F3-partial", True, ok, f"partial plan scores {result['covered_count']}/{result['total_count']}")


def test_f3_empty_plan_scores_zero():
    result = score_plan(EMPTY_PLAN)
    ok = result["coverage"] == 0.0
    assert ok, result
    _emit("F3-empty", True, ok, "empty plan scores zero coverage")
