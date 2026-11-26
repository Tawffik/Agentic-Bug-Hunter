# ABH eval harness (offline)

Owner-approved publication 2026-11-26. 13/13 checks, all offline (no provider calls). Agent-assisted work under owner direction; the harness *tests* the upstream report-gate and grounding filter (upstream code, PR #170 lineage) — it does not re-author them.

## What it covers
- **F1/F2/B1/B2 — report gate** (`test_report_gate_eval.py`): the report gate must block fabricated claims and pass honest ones. Known upstream limits proven by probes: the gate fails open when the verifier import fails (upstream is silent; the fork only warns), and a fabricated claim attached to a real evidence URL passes in both versions.
- **F3 — recon-coverage scorer** (`recon_coverage.py` + `test_recon_coverage_eval.py`): scores a recon plan's family coverage against the expected surface; validated on synthetic plans.
- **F4 — golden-template checker** (`golden_template.py` + `test_report_format_eval.py`): encodes the mechanically checkable parts of the owner's public `bb-report-template` SKILL.md (fetched 2026-11-26) as an automated checklist — mandatory sections + CONFIRMED / NOT EXECUTED labeling. Prose quality stays human-reviewed.
- **Grounding tests**: `_ground_report_output` honesty checks.

## Rerun
```bash
python3 -m pytest evals/ -q        # expected: 13 passed, no network
```
The full repo suite (`pytest tests/ -q`) is unaffected (1495 passed at publication).
