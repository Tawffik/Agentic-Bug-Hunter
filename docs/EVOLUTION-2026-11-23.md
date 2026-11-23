# Evolution Cycle — 2026-11-23

A full self-audit, evidence-first gap analysis, external research pass, and two
shipped improvements. Every claim below is backed by a command, test, or artifact
in this repo. Nothing was installed globally; no target was contacted.

## 1. What was inspected (and what was not)

**Inspected**
- Repo tree, git log (`42f9412` head), `AGENTS.md`, `README.md`, `OPENCODE.md`,
  `docs/{CAPABILITY-GAPS,MASTER_PLAN,TODOS,KNOWLEDGE-UPGRADE-2026-11,phase1-engine-validation}.md`.
- Core runtime: `bughunter/{agent,engine,brain,serve}.py`, `tools/{hunt,validate,validate_core,verifier,swarm,oracle,lead_board,self_audit,js_analyzer,cors_scanner,jwt_scanner,secrets_hunter,param_discovery,scope_checker,safe_http}.py|sh`,
  `tools/verifiers/*`, `memory/*`, `tests/benchmark/*`.
- Recon/scanner scripts (`recon_engine.sh`, `vuln_scanner.sh`), CI workflows,
  tests (1362 baseline), findings artifacts (`findings/aiven.io/*`, `findings/okg-cardano-verifymessage`),
  recon artifacts (`recon/tiktok.com`, `bughunter/recon/{tiktok.com,pipopay.com,soundon.global,temu.com}`),
  and the real hunt plan `docs/TIKTOK-HUNT-PLAN.md`.
- `hunt-memory/journal.jsonl` (synthetic/regression entries, not real target outcomes).

**Not inspected**
- Full 333-tip / Notion corpora content line-by-line (`knowledge/*`); only their
  indexes/structure and provenance doc.
- Private repos referenced by the master plan (BugBountyCI, targets-recon-results),
  external target systems, and any real user accounts.
- `node_modules/` and generated caches.

## 2. Baseline (before any change)

| Metric | Value |
|---|---|
| Tests | 1362 passed, 0 failed |
| Self-audit health | 63/100 (driven by 40/104 external binaries present) |
| Advertised agent network tools | 13 |
| Wired agent network tools | 2 (`run_recon`, `run_vuln_scan`); 11 returned TOOL UNAVAILABLE |
| Generic two-identity IDOR/BOLA engine | none (only `h1_idor_scanner.py`, HackerOne-specific) |
| Verifier benchmark | recall 1.0, precision 1.0, FP 0 |
| Authz discovery benchmark | none |

## 3. Genuine weaknesses found

| # | Weakness | Evidence | Impact |
|---|---|---|---|
| 1 | **Advertised agent tools were dead** | Runtime check: 11/13 backends missing in `hunt.TOOL_BACKENDS`; `docs/phase1-engine-validation.md` already noted `hunt.py --agent` was stale and the loop Ollama-only | The autonomous path promised JS mining, secrets, params, CORS, JWT, API authz, CMS/RCE, sqlmap and delivered only recon + one scanner |
| 2 | **No generic object-level authorization differential** | `docs/CAPABILITY-GAPS.md` says "nothing auto-generates IDOR/auth tests"; only H1-specific scanner; TikTok plan lists "two accounts required" as the hard blocker for the only promising surface | IDOR/BOLA — the #1 paid web2 class — remained manual after session capture |
| 3 | **Self-audit could not see dead wiring** | `self_audit.py` only checked external binaries, docs, and tests | A capability regression was invisible to the evolution loop |
| 4 | **Benchmark direct run was broken** | `python3 tests/benchmark/score.py` → `ModuleNotFoundError: tools` | The documented precision/recall gate could not run outside pytest |
| 5 | **Similarity-only authz checks are FP-prone** | Autorize-style tools flag `/api/me` (each user sees own data); the repo's own triage rules require two identities + a victim marker | A naive tool would inflate N/A submissions |
| 6 | **Unauth surface maturity is a real ceiling** | `docs/TIKTOK-HUNT-PLAN.md`: 5,718 subs → 1,644 live URLs, 0 findings; signed APIs (`a_bogus`), server-side sessions, edge allowlists | Better scanners alone will not break signed/authenticated targets; need session capture + request replay |

## 4. External research (what changed the design)

| Source | What was taken | What was rejected |
|---|---|---|
| `dub-flow/sessionprobe` (GitHub) | Multi-threaded URL replay with a supplied session, dedupe, filter-by-length, proxy support — confirms the operational need | It is single-session access checking, not a differential; no cross-identity oracle |
| Burp **Autorize** (industry standard) | A/B replay + control response concept | GUI-bound; similarity-only verdicts create the `/api/me` FP class |
| `xbow-engineering/validation-benchmarks` | Canary-flag benchmarking and discovery/validation separation (already adopted in `tests/benchmark`) | Saturated public labs; treated as a floor, not a discriminator |
| `usestrix/strix` | Multi-agent orchestration, validation through real PoCs, agent-ready skills | Heavy runtime; this repo already has a ReAct loop and a deterministic verifier — installing another agent would duplicate |
| `aliasrobotics/cai` | Framework patterns for agent + tool guardrails | Not needed; existing scope/audit/method guards are stronger for this harness |
| `protectai/vulnhuntr` | Static LLM-assisted discovery | Not a replacement for runtime authz proof; could be a future SAST input |
| HackerOne/Bugcrowd public methodology | Two-account evidence discipline, EMPTY/OWN/OTHER control states | — |

Design conclusion: build the missing **headless differential oracle** natively,
with the repo's existing scope guard and verifier, rather than add another scanner.

## 5. Shipped changes

### A. `tools/authz_diff.py` + `/authz-diff`

- Inputs: `--recon-dir` (urls/with_params, api_endpoints, js/endpoints) or `--har`.
- Identities: header files (JSON, Playwright storage-state, `K: V` lines), inline
  cookie/bearer, optional A baseline.
- Per URL: A → B → anonymous control; single-hop; scope-checked before sockets.
- Classification: `CROSS_USER_MARKER`, `PUBLIC_EXPOSURE`, `IDENTICAL_ACROSS_IDENTITIES`,
  `SAME_SCHEMA_DIFFERENT_DATA`, `DISTINCT_PER_USER`, `PUBLIC`, `ENFORCED`, `UNKNOWN`, `SKIPPED`.
- FP controls: anonymous control, object-ref requirement, per-user marker control,
  HTML skip, volatile JSON key normalization, substantive-body threshold.
- `--confirm` runs the existing IDOR verifier in memory; only a marker-based oracle
  can confirm. Output is redacted metadata (no headers/bodies).
- Writes `recon/<target>/authz/leads.txt` so `lead_board.py ingest` routes leads to
  `hunt-idor` (new path-object-ID route).

### B. Agent tool wiring + contract tests

- Implemented 10 missing `hunt.py` backends (JS analysis, secrets, param discovery,
  CORS, JWT, CMS/RCE nuclei sweeps, sqlmap targeted/request-file, authz diff).
- Replaced the dead `run_api_fuzz`/`run_post_param_discovery` advertisements with
  the real `run_authz_diff`; removed the one tool that had no honest implementation.
- CORS runs in-process so authenticated cookies never appear in a subprocess argv.
- `self_audit.py` now AST-checks `TOOL_BACKENDS` against real functions and reports
  dead tools as a high-severity gap.
- `tests/test_agent_tool_contract.py` fails if an advertised tool loses its backend.

### C. Credential-persistence hardening (found during the audit)

- `validation.json` was written raw by both validators, including verifier traces
  with identity request headers and cookies inside `curl_poc`. Both writers now
  persist `redact_obj(payload)`; tests assert secret markers and PII never hit disk.
- `run_swarm` interpolated target/scope values into a shell string; it now uses
  an argv list. Test asserts the argv shape.
- `sqlmap` backend confirmation matched the substring "injectable", which also
  matches "not injectable"; it now requires sqlmap's positive "is vulnerable"
  wording (unit-tested).

### D. Measurement

- `tests/benchmark/authz_score.py`: two-user target, 1 real BOLA, 6 controls.
  Result: recall 1.0, confirmed_fp 0, marker_lead_fp 0, verdict_accuracy 1.0.
- `tests/test_authz_diff.py`: 11 unit/integration tests (including closed-loop
  discovery → IDOR verifier → `validated_finding`).
- `tests/test_hunt_react_backends.py`: offline JS/JWT/authz backend + argv-shape tests.
- `tests/test_validation_redaction.py`: durable validation output never stores secrets.
- Fixed `tests/benchmark/score.py` direct execution.

## 6. After metrics

| Metric | Before | After |
|---|---|---|
| Tests | 1362 | **1390 passed** |
| Dead advertised agent network tools | 11/13 | **0/12** |
| Generic authz differential | absent | **shipped + benchmarked** |
| Authz benchmark | n/a | **recall 1.0 / confirmed FP 0 / marker lead FP 0** |
| Verifier benchmark | 1.0 / 0 FP | **unchanged 1.0 / 0 FP** |
| Self-audit blind spot | dead tools invisible | **reported as high-severity gap** |
| Docs/commands | no `/authz-diff` | **command + skill reference + tool docs + CHANGELOG** |

## 7. Residual risks and honest limits

- **Authz engine is not a proof machine.** Similarity leads (`IDENTICAL_…`,
  `SAME_SCHEMA_…`) still need human/verifier ownership reasoning. Only marker-based
  cross-user reads are confirmed.
- **Object IDs must be A-owned.** The tool deliberately does not guess IDs.
- **GET only.** Write-method BOLA (DELETE/PUT/PATCH) needs an approval-gated flow;
  the method matrix is documented but not automated.
- **Session acquisition is still the hard blocker** on signed/authenticated targets
  (TikTok evidence). `browser_capture.py` + storage-state ingestion reduces friction,
  but account provisioning/signing reversal remains manual by design.
- **No cache-deception, WebSocket/PostMessage runtime, multimodal LLM, or bridge
  audit automation yet.** These remain documented-only or partial.
- **The hunt journal is synthetic.** `oracle.py` has no real outcome data to learn
  from until real hunts record `confirmed`/`rejected` outcomes.

## 8. Next candidates (researched, not shipped)

| Candidate | Why | Cost | Risk |
|---|---|---|---|
| Cache-deception probe (authenticated URL + `.css/.js`, cache hit + marker) | High-payout class; currently docs-only; shares authz infrastructure | Medium | Cache poisoning side effects; must be read-only, no-store |
| WebSocket/PostMessage runtime harness | Cross-site WS hijack and client authz gaps are invisible to HTTP scanners | Medium | Needs Playwright + origin control |
| Request-signing replay harness (client-reverse) | Signed APIs blocked the TikTok hunt | High | Target-specific, fragile |
| API-spec → authz test generation | `spec_ingest.py` classifies object params but does not generate BOLA tests | Low–Medium | Wrong-tenant object IDs are unsafe; only A-owned inputs allowed |
| Retest harness for past findings | Continuous monitoring / regression | Low | None |
| Pre-submit duplicate search (H1 Hacktivity by endpoint/title) | Reduces N/A/duplicate ratio | Low | Public search is incomplete; must not imply certainty |

## 9. Reproduction

```bash
python -m pytest -q
python tests/benchmark/score.py
python tests/benchmark/authz_score.py
python bughunter/tools/self_audit.py audit
python bughunter/tools/authz_diff.py --help
```
