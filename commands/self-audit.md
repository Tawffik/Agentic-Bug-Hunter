---
description: Self-audit the agent — capability inventory, coverage gaps, test-regression drift, and an improvement ledger with measured before/after metrics. Usage: /self-audit [audit|baseline|drift|record|ledger]
---

# /self-audit

The agent inspecting itself: what it can do, what is missing, and whether a
change broke anything.

```bash
# Capability inventory + gaps (read-only):
python3 bughunter/tools/self_audit.py audit

# Same, plus run the suite and check for regressions against the baseline:
python3 bughunter/tools/self_audit.py audit --run-tests --json

# Record the current test results as the regression baseline:
python3 bughunter/tools/self_audit.py baseline

# Regression gate — exits non-zero if failures rose or passing tests dropped:
python3 bughunter/tools/self_audit.py drift

# Log an improvement with measured metrics (deltas computed vs the last entry):
python3 bughunter/tools/self_audit.py record \
  --title "add OpenAPI spec ingestion" \
  --metric tests_passed=1307 --metric tools=83 --note "contract-driven API surface"

# Review the improvement history:
python3 bughunter/tools/self_audit.py ledger
```

## What the audit checks

- **Capabilities** — counts of tools, skills, agents, commands, tests.
- **External tools** — every binary in `external_arsenal.sh` vs what is on `PATH`.
- **Documentation coverage** — tool files missing from `tools/README.md`.
- **Regression** — current pass/fail vs the stored baseline (failures rose or
  passes dropped ⇒ regression).
- **Health score** — composite 0–100 (tests, external coverage, docs).

State (baseline + improvement ledger) lives under
`bughunter/memory/self-audit/` at `0600`.

## Evolution loop

1. `audit` → find the biggest gap.
2. Implement + test the fix.
3. `record` the measured result.
4. `baseline` when the new results are green; `drift` in CI to catch regressions.
