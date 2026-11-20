---
name: web3-fuzz
description: Generate and run a stateful Solidity fuzz suite (Echidna/Medusa/Foundry) for a Foundry or Hardhat project. Use for invariant testing, property-based fuzzing, handler scaffolding, coverage-driven fuzzing, or converting a fuzzer counterexample into a Foundry PoC. Derived from Pashov Audit Group's MIT-licensed fizz skill; adapted for this harness.
---

# WEB3 FUZZ — STATE FUL INVARIANT SUITE

Turn a protocol into a fuzzable state machine, find invariant violations, then
convert each counterexample into a minimal Foundry PoC. Fuzzing proves the
counterexample exists; it never proves safety when coverage is low.

**Lead-only rule:** a fuzzer violation is a LEAD until the exact call sequence is
reproduced in a target-local Foundry test and the impact is quantified.

**Attribution:** templates, scripts, and agent prompts are adapted from
[Pashov Audit Group Skills — fizz](https://github.com/pashov/skills/tree/main/fizz)
(MIT). See `UPSTREAM.md`.

---

## WHEN TO USE

- A protocol has accounting invariants (`totalAssets`, `totalSupply`, shares,
  debt, collateral, rewards) but tests only cover happy paths.
- You have a hypothesis "can a sequence of calls break X?" and need to explore it.
- You want Medusa/Echidna coverage before writing an invariant claim.
- A fuzzer found a counterexample and you need a Foundry PoC.

Do not use on an unauthorized target or send mainnet transactions.

## REQUIREMENTS

| Tool | Required | Check |
|---|---|---|
| `forge` | yes | `forge --version` |
| `medusa` | yes | `medusa --version` |
| `echidna` | recommended | `echidna --version` |
| `node` | yes (scripts) | `node --version` |

Install the stack: `./install_tools.sh --with-web3`. Detect other chains:
`bash bughunter/tools/chain_audit_env.sh <project>`.

If a tool is missing, stop and report exactly which one; do not silently skip.

## OUTPUT LAYOUT

- `{PROJECT}/test/fizz/` — Solidity suite (`Base.sol`, `Snapshots.sol`,
  `Properties.sol`, handlers, `FuzzTester.sol`, `FoundryTester.sol`)
- `{PROJECT}/fizz_data/` — ABI inventory, entry-point selection, protocol notes,
  coverage targets, corpora, run logs
- `{PROJECT}/echidna.yaml`, `{PROJECT}/medusa.json` — fuzzer configs

`{SKILL_DIR}` = directory containing this `SKILL.md` (e.g.
`skills/web3-fuzz`). `{PROJECT}` = target repo root. `{SUITE}` = `test/fizz`.
`{META}` = `fizz_data`.

---

## STEP 0 — DETECT AND CHECK

```bash
bash bughunter/tools/chain_audit_env.sh {PROJECT}
forge --version; medusa --version; echidna --version || true
```

If Hardhat: ensure `hardhat.config.*` exists and `node_modules` is installed.
If Foundry: read `foundry.toml`; note `via_ir`, `src`, `out`.

Read `references/template-map.md` before generating anything.

## STEP 1 — COMPILE AND EXTRACT ABIs

```bash
cd {PROJECT} && forge build
node {SKILL_DIR}/scripts/extract_abis.js {PROJECT} --meta-dir {META}
```

If Foundry is absent but Hardhat is present, create a compatible `foundry.toml`
with `{SKILL_DIR}/scripts/ensure_foundry.sh {PROJECT}` first, then rebuild.

## STEP 2 — UNDERSTAND THE PROTOCOL

Read the in-scope source, deployment scripts, tests, and any `x-ray/x-ray.md`.
Write `{META}/protocol-understanding.md` with:

- deployment order, constructor args, post-deploy initialization
- actors/roles and permissioned actions
- external entry points vs internal plumbing
- value flows, shares/debt/reward accounting
- candidate invariants (conservation, solvency, monotonicity, access, state machine)

Do not invent a deployment flow when the repo already has one.

## STEP 3 — SELECT ENTRY POINTS

Read `references/selection-policy.md`.

```bash
node {SKILL_DIR}/scripts/select_functions.js {PROJECT} \
  --contracts {META}/contracts.json \
  --selection {META}/entry-point-selection.json --meta-dir {META} --auto
```

Interactive mode (omit `--auto`) opens a local picker. Keep core user flows and
high-impact permissioned actions; exclude views and one-time bootstrap. Mark
`primary` vs `secondary` for the dispatcher tier.

## STEP 4 — SCAFFOLD

```bash
node {SKILL_DIR}/scripts/generate_suite.js {PROJECT} \
  --suite-dir {SUITE} --meta-dir {META}
```

This copies templates (including `utils/MockERC20.sol`), writes fuzzer configs,
and creates one handler stub per selected contract.

## STEP 5 — WIRE SETUP AND HANDLERS

Read `references/setup-playbook.md`, `references/handler-patterns.md`, and
`references/template-map.md`.

Edit `{SUITE}/Base.sol::setup()`:
- deploy/wire real contracts; use proxies exactly as production does
- use `MockERC20` only for external tokens outside the deployment graph
- fund actors and grant roles/approvals
- add ghost state only where a property needs it

Then refine each `{SUITE}/handlers/<Contract>Handler.sol`:
- clamped handler for realistic ranges; unclamped variant for boundary stress
- caller switching via `asActor` / `asAdmin`
- ghost updates **after** the external call succeeds
- no assertions that merely restate the implementation

```bash
cd {PROJECT} && forge build
```

Do not proceed until the scaffold compiles.

## STEP 6 — COVERAGE LOOP (MEDUSA)

If `via_ir = true`, create a fuzz profile:

```bash
bash {SKILL_DIR}/scripts/setup_fuzz_profile.sh {PROJECT}
```

Use `FOUNDRY_PROFILE=fuzz forge build` when the script reports `no-ir` or
`ir-no-opt`; otherwise use `forge build`.

Run, inspect, adjust handlers, rebuild:

```bash
node {SKILL_DIR}/scripts/run_medusa.js {PROJECT} --meta-dir {META} --coverage-mode
```

Write per-contract targets and skip reasons to `{META}/coverage-targets.md`.
Targets: core 80%+, access control 60%+, periphery 50%+ (lower by 10% for
`ir-no-opt`). Cap unguided cycles at 3. Low coverage means the absence of a
violation proves nothing.

## STEP 7 — GENERATE INVARIANTS

Read `references/property-generation.md`. Use five discovery lenses (agent
prompts in `{SKILL_DIR}/agents/invariant-discovery/`):

1. **Conservation** — sum of parts equals tracked whole for every aggregate.
2. **Round-trip / rounding** — inverse operations, directional rounding, zero
   shares for non-zero assets.
3. **State transition** — postconditions, monotonicity, entity counts, modes.
4. **Adversarial profit** — value extraction, DoS, griefing, edge states.
5. **Protocol type** — vault/lending/AMM/staking-specific invariants.

Write:
- ghosts in `Base.sol` + updates in handlers
- before/after snapshots in `Snapshots.sol`
- `property_*` functions in `Properties.sol`
- harness contracts only for genuinely private/internal state

Every property must be falsifiable by a concrete call sequence. Do not write
`assertTrue(true)` or properties that restate a require in the target.

## STEP 8 — RUN AND TRIAGE

```bash
cd {PROJECT} && forge build
node {SKILL_DIR}/scripts/run_medusa.js {PROJECT} --meta-dir {META} --timeout 600
node {SKILL_DIR}/scripts/run_echidna.js {PROJECT} --meta-dir {META} --timeout 600
```

For each violation:
1. Read the minimized call sequence; identify the first failing call.
2. Reproduce it in `{SUITE}/FoundryTester.sol` with `forge test --match-test ... -vvvv`.
3. Compare pre/post balances, shares, debt, or access state.
4. Kill it if a guard, clamp, or setup assumption makes it unreachable.
5. If real, write a minimal standalone PoC under `test/` (not just the fuzzer
   harness) and quantify the loss.

Keep run logs in `{META}/corpus_medusa/` and `{META}/corpus_echidna/`.

## STEP 9 — REPORT

Use the existing `skills/web3-audit/references/validation-gates.md` and
`skills/report-writing/SKILL.md`.

- Title: `[Class] in [contract/function] allows [actor] to [impact]`
- Evidence: minimized call sequence + Foundry `-vvvv` trace + numeric delta
- Status: `CONFIRMED` only when the standalone PoC passes on a pinned fork or
  local harness; otherwise `LEAD — NOT EXECUTED`
- Never claim "fuzzing proves the protocol is safe" from low coverage

## QUICK COMMANDS

```bash
# ABI + selection + scaffold
node $SKILL_DIR/scripts/extract_abis.js $PROJECT --meta-dir fizz_data
node $SKILL_DIR/scripts/select_functions.js $PROJECT --auto
node $SKILL_DIR/scripts/generate_suite.js $PROJECT

# run
node $SKILL_DIR/scripts/run_medusa.js $PROJECT --meta-dir fizz_data --coverage-mode
node $SKILL_DIR/scripts/run_echidna.js $PROJECT --meta-dir fizz_data --timeout 600

# targeted repro
forge test --match-contract FoundryTester -vvvv
```
