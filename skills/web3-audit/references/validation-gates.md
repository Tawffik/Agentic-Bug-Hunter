# Web3 finding validation — four gates

Adapted from Pashov Audit Group's MIT-licensed `solidity-auditor` judging
protocol (https://github.com/pashov/skills). Use after a candidate is
reproduced with a PoC and before writing the report. Fail any gate →
**REJECTED** or **DEMOTE** to lead; later gates are not evaluated.

## Gate 1 — Attack execution

Trace the claimed path from caller to harm. Read every guard, check, modifier,
and constraint on that path. Does any of them interrupt the attack before harm?

- A specific guard/check interrupts the exploit step → **REJECTED** (quote it)
- The interruption is speculative ("the deployer probably sets X") → clears

## Gate 2 — Reachability

Prove the vulnerable state exists in a live or faithfully forked deployment.

- Structurally impossible (enforced invariant) → **REJECTED**
- Requires privileged actions outside normal operation → **DEMOTE**
- Reachable through normal usage or common token behavior → clears

## Gate 3 — Trigger

Prove an unprivileged actor can execute the attack.

- Only a trusted role can trigger → **DEMOTE**
- Unprivileged actor triggers profitably → clears
- Harm requires a malicious admin acting against documented intent → **REJECT**
  unless the body names an unprivileged amplifier: race, retroactive sweep,
  asymmetric formula, or missing access/init guard.

## Gate 4 — Impact

Prove material harm to an identifiable victim.

- Self-harm only → **REJECTED**
- Dust-level, non-compounding → **DEMOTE**
- Material loss to an identifiable victim → **CONFIRMED**

## Confidence

Start at **100**; deduct:
- partial attack path **-20**
- bounded, non-compounding impact **-15**
- requires specific but achievable state **-10**

`>= 75` → description + fix. `< 75` → description only.
Use the repo's CVSS/report rules for the final score; confidence is a triage
gate, not a payout estimate.

## Lead promotion (before finalizing)

- **Cross-contract echo** — same root cause confirmed in one contract →
  promote where the identical pattern appears.
- **Multi-agent convergence** — 2+ independent analyses flag the same area and
  the lead was demoted (not rejected) → promote to finding.
- **Partial-path completion** — path is reachable and unguarded; only the full
  trace is incomplete → finding at 75, description only (no fix block).

## Do not report

- Linter/compiler issues, gas micro-opts, naming, NatSpec.
- Admin privileges by design; missing events; centralization without an exploit.
- Implausible preconditions. For contracts accepting arbitrary tokens,
  fee-on-transfer, rebasing, and blacklisting **are** plausible.
- A stale-root / EB-drift / liquidation-liveness issue already listed in the
  program's Known Issues.
- A pattern match from Slither/Solodit/DeFiHackLabs without a target-local PoC.

## Safe patterns (do not flag without a new path)

`unchecked` in Solidity 0.8+ with correct reasoning; explicit narrowing casts
that revert; `MINIMUM_LIQUIDITY` burn on first deposit; `SafeERC20`; a working
`nonReentrant` (only flag cross-contract bypasses); two-step admin transfer;
consistent protocol-favoring rounding unless it compounds or rounds to zero.

## Evidence table for the report

| Step | Action | Evidence | Status |
|---|---|---|---|
| 1 | A reads/affects B's object | raw request/trace showing B's data/loss | CONFIRMED |
| 2 | Enumerate adjacent IDs at scale | 3 samples + count, redacted | NOT EXECUTED |
| 3 | Full fund extraction | PoC balance delta | CONFIRMED |

Severity is set by **confirmed** steps only. A chain with an unexecuted step is
a lead, not a critical.
