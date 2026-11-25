"""Golden report-template checker for the ABH eval harness (fixture F4).

Encodes the mechanically checkable parts of the owner's public
bb-report-template skill (Tawffik/bb-report-template, SKILL.md, fetched
2026-11-26) as an automated checklist, per agent-eval-rubric.md:
"قراءة bb-report-template من ريبوهات المالك العامة وتحويلها لقائمة فحص آلية".

Checks presence of mandatory sections and the CONFIRMED / NOT EXECUTED
labeling contract. Prose quality stays human-reviewed per the rubric.
"""

from __future__ import annotations

import re

# Mandatory sections from the golden template. Each entry: (id, regex over the
# report text, human label). Regexes tolerate common heading styles.
REQUIRED_SECTIONS: list[tuple[str, str, str]] = [
    ("title", r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?title(?:\*\*)?\s*:", "factual title"),
    ("asset", r"(?im)\basset\b\s*[:|]", "metadata: exact asset"),
    ("severity", r"(?im)\bseverity\b\s*[:|]", "metadata: severity"),
    ("cwe", r"(?im)\bCWE\b", "metadata: CWE"),
    ("cvss", r"(?im)\bCVSS\b", "metadata: CVSS score + vector"),
    ("date", r"(?im)\b\d{4}-\d{2}-\d{2}\b", "metadata: date YYYY-MM-DD"),
    ("summary", r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?summary", "summary section"),
    (
        "details",
        r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?(vulnerability\s+details|description)",
        "vulnerability details section",
    ),
    (
        "steps",
        r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?(steps\s+to\s+reproduce|proof\s+of\s+concept|poc)",
        "steps to reproduce / PoC",
    ),
    ("impact", r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?impact", "impact section"),
    ("remediation", r"(?im)^\s*(?:#{1,3}\s*)?(?:\*\*)?remediation", "remediation section"),
]

_CHAIN_TABLE_RE = re.compile(r"(?im)^\s*\|.*\bstep\b.*\|.*\bstatus\b", re.IGNORECASE)
_LABEL_RE = re.compile(r"\b(CONFIRMED|NOT EXECUTED)\b")


def check_report(report_text: str) -> dict:
    """Return per-section presence plus labeling-contract findings."""
    text = report_text or ""
    sections = {
        section_id: bool(re.search(pattern, text))
        for section_id, pattern, _ in REQUIRED_SECTIONS
    }
    missing = [section_id for section_id, ok in sections.items() if not ok]

    has_chain_table = bool(_CHAIN_TABLE_RE.search(text))
    labels = set(_LABEL_RE.findall(text))
    labeling = {
        "has_chain_table": has_chain_table,
        "has_confirmed_label": "CONFIRMED" in labels,
        "has_not_executed_label": "NOT EXECUTED" in labels,
        # Golden rule: a multi-step chain table must never blur confirmed and
        # assumed; it must carry explicit status labels.
        "chain_table_labeled": (not has_chain_table) or bool(labels),
    }

    present = sum(1 for ok in sections.values() if ok)
    return {
        "sections": sections,
        "missing": missing,
        "present_count": present,
        "total_count": len(REQUIRED_SECTIONS),
        "coverage": present / len(REQUIRED_SECTIONS),
        "labeling": labeling,
        "pass": not missing and labeling["chain_table_labeled"],
    }
