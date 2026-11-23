# Agent Capability Gaps — Status Ledger

Research basis: 2026 conference record (DEF CON 34 / Black Hat USA / AI Village)
and the arXiv corpus (survey `2607.02605`; SoK `2604.05719`; ATOBench
`2608.12996`; BountyBench `2505.15216`; MAPTA `2508.20816`; AgentFlow
`2604.20801`; Harness Matters `2610.28802`; Big Enough to Break Out `2609.10780`).
Status reflects the repo as of the P0/P1/P2 implementation.

Legend: **DONE** · **PARTIAL** · **OPEN**

## Evidence & validation

| Gap | Status | Where |
|---|---|---|
| Adversarial falsifier (disprove before report) | DONE | `tools/adversarial_validator.py`, `agents/falsifier.md` |
| Verifier class coverage (7 → 17) | DONE | `tools/verifiers/` |
| Four-part evidence contract | DONE | `tools/evidence_contract.py`, `validate_core.py` |
| Report path blocks unproven/falsified | DONE | `is_report_ready()` + `tests/test_report_gate.py` |
| Deception-resistance controls | PARTIAL | adversarial public/baseline/own-object checks; full paired-ATO simulation still manual |
| Business-logic canary placement | OPEN | use `verifiers/business_logic.py` sequence+invariant today |

## Harness & orchestration

| Gap | Status | Where |
|---|---|---|
| App model before hunting (endpoints/auth/objects) | DONE | `tools/app_model.py` |
| Central dedup of endpoints | DONE | `app_model.endpoint_key()` |
| Fresh context per stage | DONE | `tools/stage_handoff.py`, `agents/autopilot.md` |
| Planning/commitment state | DONE | `tools/planning_ledger.py` |
| Model-matched plain-agent baseline | OPEN | needs a private task set (see below) |
| Harness tunability/synthesis | OPEN | advanced; not required for L4 |

## Knowledge & retrieval

| Gap | Status | Where |
|---|---|---|
| Prior-art retrieval | DONE | `tools/prior_art_rag.py` (offline TF-IDF) |
| Relevance gate (avoid misleading retrieval) | DONE | score floor + min token overlap |
| Dynamically maintained CVE KB | OPEN | refresh `knowledge/` + lead-board intel |

## Model & cost

| Gap | Status | Where |
|---|---|---|
| Cost-aware per-stage routing | DONE | `tools/model_router.py` |
| $/solve accounting | DONE | `CostLedger.per_solve()` |
| Multi-model ensemble/union | OPEN | run staged handoffs across ≥2 models |
| Refusal/guardrail ops playbook | OPEN | document per-provider behavior |

## Agentic-app / LLM surface

| Gap | Status | Where |
|---|---|---|
| LLM exfil canary verifier | DONE | `tools/verifiers/llm_exfil.py` |
| 2026 techniques (memory poisoning, delayed exec, cross-agent, PleaseFix, 9 channels) | DONE | `skills/agentic-app-audit`, `skills/llm-redteam` |
| MCP supply-chain / rug-pull checks | DONE | `skills/mcp-server-audit` |
| Agent supply-chain scanner | DONE | `tools/agent_supply_chain_scan.py` |

## Evaluation

| Gap | Status | Where |
|---|---|---|
| Deterministic verifier benchmark (recall/FP) | DONE | `tests/benchmark/score.py` |
| Evidence-chain / process metrics | DONE | `tools/process_metrics.py` |
| Stage partial credit | DONE | `process_metrics.stage_credit()` |
| Private novel benchmark (non-public targets) | OPEN | must be built against authorized, unpublished targets |
| Contamination management | OPEN | never rank on public/saturated sets |

## Security & safety (of the agent)

| Gap | Status | Where |
|---|---|---|
| Single egress choke point + CI guard | DONE | `verifiers/base.py`, `tests/test_egress_choke_point.py` |
| Least-privilege / blast-radius model | PARTIAL | agent frontmatter; formalize per-tool caps |
| Runtime watchdog/replay | OPEN | audit log exists; add action replay |

## Ops / coverage

| Gap | Status | Where |
|---|---|---|
| External tool coverage | PARTIAL | `external_arsenal.sh`; install remaining binaries |
| Mobile runtime verification | OPEN | `--with-pro` install (adb/frida) |

## Definition of done (remaining for full L4)

1. Private, non-public benchmark with process metrics reported alongside the
   verifier floor.
2. Model-matched plain-agent baseline on that set.
3. One production `planning_ledger` + `stage_handoff` run wired into autopilot.
4. Least-privilege table per agent + runtime action replay.
5. `self_audit` health ≥ 85 (install missing tools).
