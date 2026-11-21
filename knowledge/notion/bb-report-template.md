# SKILL: Bug Bounty Report Template — Living Standard

**Name:** `bb-report-template`  
**Version:** 1.0  
**Source:** Notion — *Bug Bounty Report Template — Living Standard*  
**Purpose:** Produce high-credibility reports that separate **confirmed** evidence from **assumed** chain steps. Copy the master template per finding; never edit the skill template in place for a specific bug.

## When to use

- Drafting any program submission
- Converting LEAD evidence into a report package
- After triager feedback (update living lessons in version log)

## Title formula

`[Vulnerability type] in [exact component/endpoint] allows [specific attacker-achievable impact]`

- No emotional language
- Exact component, not only domain
- Impact as an action, not a category
- Respect platform field rules (some want endpoint outside the title)

## Metadata block

| Field | Value |
| --- | --- |
| Asset | exact URL / repo / binary |
| Severity | Critical/High/Medium/Low + platform scale (e.g. P1–P5) |
| CWE | |
| CVSS 3.1 | score + vector |
| Revision tested | commit / build / "as of date" |
| Date | YYYY-MM-DD |

State severity as **confirmed**. Note separately what an unproven chain step *could* become. Overclaiming kills credibility.

## Summary (2–4 sentences)

Template:  
`[Component] is supposed to [intended security property]. It fails to [missing check], which means [attacker action] results in [concrete consequence] without [prerequisite the attacker shouldn't need].`

## Vulnerability details

- Exact function/endpoint/file/line when possible
- What check exists, what is missing, why the gap allows bypass
- Cite standard/spec when useful
- Note related functions that behave correctly (strengthens credibility)

## Steps to reproduce / PoC

Numbered, copy-pasteable, with environment (revision, tool versions).

Prefer pasted terminal/text over screenshots. Screenshots only for UI states text cannot show.

## Attack chain table (mandatory when multi-step)

| Step | Description | Status |
| --- | --- | --- |
| 1 | … | CONFIRMED |
| 2 | … | CONFIRMED |
| 3 | … | NOT EXECUTED (reason) |

Never blur confirmed and assumed.

## Impact

- Worst case / if chain completed: concrete consequence
- Confirmed-only: narrower proven consequence

## Remediation

Ordered, actionable: root cause fix → defense-in-depth → containment → structural fix.

## Scope & disclosure integrity notes

Use when scope is uncertain or steps were deliberately not executed. State clearly that no unauthorized access to real accounts/data was performed.

## Rejection-reason checklist (before submit)

- [ ] Asset on **current** in-scope list
- [ ] Not a cross-channel duplicate
- [ ] Every step labeled confirmed or not-executed
- [ ] PoC re-run before submission
- [ ] Severity matches proven impact
- [ ] No single evidence implying two different tests
- [ ] Factual title
- [ ] Concrete impact (not only CWE)
- [ ] Remediation actionable
- [ ] Unexecuted steps stated plainly

## Agent output contract

1. Emit draft using the master sections above
2. Force CONFIRMED vs NOT EXECUTED labels on every chain step
3. Refuse to claim severity above proven evidence
4. Attach minimal redacted proof artifacts list
