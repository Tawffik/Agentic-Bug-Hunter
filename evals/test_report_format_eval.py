"""Eval harness — report-format fixtures (F4) + output-grounding checks.

Rubric dimensions: report completeness vs the golden template (30%) and
honesty of claims (20%, mechanically testable part only).

F4 checks a report text against evals/golden_template.py, the automated
checklist derived from the owner's public bb-report-template skill.
Grounding checks exercise brain.Brain._ground_report_output offline with
synthetic evidence/report pairs — no provider calls, no network.

Each case prints one EVAL_RESULT JSON line for the future
baseline-vs-candidate runner. These fixtures measure the deterministic
checker and grounding logic only — not model quality.
"""

import json
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for path in (os.path.join(REPO_ROOT, "bughunter"), os.path.join(REPO_ROOT, "bughunter", "tools")):
    if path not in sys.path:
        sys.path.insert(0, path)

import brain  # noqa: E402
from evals.golden_template import check_report  # noqa: E402


def _bare_brain():
    b = brain.Brain.__new__(brain.Brain)
    b.enabled = True
    b.model = "eval-offline"
    return b


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


FULL_REPORT = """## REPORT 1: Reflected XSS in /search

**Title:** Reflected XSS in /search allows attacker to run JavaScript in victim session

| Field | Value |
| --- | --- |
| Asset | https://lab.example/search |
| Severity | Medium — CVSS 3.1: 6.1 (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N) |
| CWE | CWE-79 |
| Date | 2026-11-25 |

## Summary
The search endpoint is supposed to HTML-encode user input. It fails to encode
the q parameter, which means a crafted link results in script execution in the
victim's browser without any authentication.

## Vulnerability details
The q parameter is reflected unencoded in the results page. CWE-79.

## Steps to reproduce
1. Open https://lab.example/search?q=<script>alert(1)</script>
2. Observe the alert firing.

## Attack chain
| Step | Description | Status |
| --- | --- | --- |
| 1 | Reflection confirmed | CONFIRMED |
| 2 | Session theft | NOT EXECUTED (would require real victim) |

## Impact
Confirmed: arbitrary JS execution in a victim's session on lab.example.

## Remediation
HTML-encode the q parameter on output; add a Content-Security-Policy header.
"""


def test_f4_full_report_passes_golden_checklist():
    result = check_report(FULL_REPORT)
    assert result["pass"], f"missing: {result['missing']}, labeling: {result['labeling']}"
    _emit("F4-full", True, result["pass"], "complete synthetic report satisfies golden checklist")


def test_f4_missing_sections_detected():
    # Drop the remediation section and the CWE line.
    broken = FULL_REPORT.replace("## Remediation", "## Fix-notes") \
        .replace("| CWE | CWE-79 |\n", "") \
        .replace("CWE-79", "a weakness class")
    result = check_report(broken)
    assert not result["pass"]
    assert "remediation" in result["missing"]
    assert "cwe" in result["missing"]
    _emit("F4-missing", False, result["pass"],
          "missing remediation+CWE detected: " + ",".join(result["missing"]))


def test_f4_unlabeled_chain_table_flagged():
    unlabeled = FULL_REPORT.replace("| 1 | Reflection confirmed | CONFIRMED |",
                                    "| 1 | Reflection confirmed | done |") \
        .replace("| 2 | Session theft | NOT EXECUTED (would require real victim) |",
                 "| 2 | Session theft | pending |")
    result = check_report(unlabeled)
    assert result["labeling"]["has_chain_table"]
    assert not result["labeling"]["chain_table_labeled"]
    assert not result["pass"]
    _emit("F4-chain-labels", False, result["pass"], "unlabeled multi-step chain table flagged")


EVIDENCE = """Validated finding on https://lab.example/search?q=test
GET /search?q=test HTTP/1.1
Response reflects <script>alert(1)</script> at /search
"""

GROUNDED_REPORT = """## REPORT 1: Reflected XSS in /search

**Title:** Reflected XSS in /search allows script execution

Steps: send the validated request: https://lab.example/search?q=test
The q value is reflected unencoded (payload: a script tag).
"""

INVENTED_REPORT = """## REPORT 1: SQL injection in /admin-panel

**Title:** SQL injection in /admin-panel allows data theft

Steps: visit https://lab.example/admin-panel?id=1' OR '1'='1
"""


def test_grounding_keeps_evidence_backed_report():
    b = _bare_brain()
    out = b._ground_report_output(GROUNDED_REPORT, EVIDENCE)
    ok = out != "NO_REPORTS" and "/search" in out
    assert ok
    _emit("G1-grounded", True, ok, "report using only evidence URLs is kept")


def test_grounding_drops_invented_endpoint_report():
    b = _bare_brain()
    out = b._ground_report_output(INVENTED_REPORT, EVIDENCE)
    ok = out == "NO_REPORTS"
    assert ok, f"expected NO_REPORTS, got: {out[:80]}"
    _emit("G2-invented", True, ok, "report with endpoint absent from evidence is dropped")


def test_grounding_mixed_report_keeps_only_grounded_sections():
    b = _bare_brain()
    mixed = GROUNDED_REPORT + "\n---\n\n" + INVENTED_REPORT
    out = b._ground_report_output(mixed, EVIDENCE)
    ok = out != "NO_REPORTS" and "/search" in out and "/admin-panel" not in out
    assert ok, f"unexpected: {out[:120]}"
    _emit("G3-mixed", True, ok, "mixed report keeps grounded section, drops invented one")
