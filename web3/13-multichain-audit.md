# 13 — Multichain audit addendum

The main `web3/` track is EVM-first. Use this addendum when the scope is
Solana/Anchor, Aptos Move, Sui Move, Soroban, DAML/Canton, or an L1 node client.
The same discipline applies: read the spec, map privileged paths, prove a
target-local PoC, and kill anything that is only a pattern match.

Detect the project and print exact commands:

```bash
bash bughunter/tools/chain_audit_env.sh /path/to/repo
```

## Toolchain registry

| Stack | Build | Test | Fuzz / property |
|---|---|---|---|
| EVM (Foundry) | `forge build` | `forge test -vvv` | `medusa fuzz` · `echidna . --contract FuzzTester --config echidna.yaml` |
| EVM (Hardhat) | `npx hardhat compile` | `npx hardhat test` | `npx hardhat test --grep fuzz` |
| Solana (Anchor) | `anchor build` | `anchor test` | Trident · `cargo test proptest_*` |
| Aptos Move | `aptos move compile` | `aptos move test` | boundary-value unit tests |
| Sui Move | `sui move build` | `sui move test` | `sui move test --rand-num-iters N` |
| Soroban | `stellar contract build` | `cargo test --features testutils` | `cargo +nightly fuzz run ...` · proptest |
| DAML | `daml build` | `daml test` | Daml Script boundary cases |
| L1 clients (Go/Rust) | project-specific | project-specific | unit/integration + fuzzing harness |

## Chain-specific bug classes

### Solana / Anchor
- Missing `is_signer` / owner check on an account that gates value or authority.
- PDA seed collisions or missing bump canonicalization.
- Duplicate mutable accounts (same account passed twice) corrupting accounting.
- Account re-initialization / missing `init` discriminator check.
- CPI privilege escalation or passing a malicious program id.
- Token-account confusion (wrong mint, wrong owner, fake token program).
- Close/drain leaving lamports or reusing a closed account in the same tx.
- Arithmetic on `u64` token amounts without checked math.
- Anchor constraints that validate existence but not the expected relation
  (`has_one`, `constraint = a.key() == b.key()`), and `remaining_accounts`
  validated only by count.
- PoC: `anchor test` or a Rust integration test with explicit accounts; show
  the victim's lamports/tokens moving or the invariant breaking.

### Aptos Move
- Capability leak (storing/transferring a `Cap` without the intended guard).
- Resource `abilities`: `copy`/`drop` on value-bearing resources; `key`/`store`
  on objects that should not be transferable.
- `public entry` vs `public(friend)` exposure; friend declarations widened.
- Missing `signer` authorization or accepting an arbitrary `&signer`.
- Generic type confusion / phantom type parameters used as an authorization tag.
- Module initialization and upgrade policy (compatibility, publisher).
- Object transfer/extend/delete without ownership checks.
- PoC: `aptos move test` with two signers; show cap/resource movement.

### Sui Move
- Object ownership: shared vs owned vs immutable; functions that accept an
  arbitrary owned object without checking the sender.
- Capability objects (AdminCap, TreasuryCap) transferred or made public.
- `entry` vs `public` visibility and `public(package)` widening.
- Dynamic-field / dynamic-object key collisions or stale children.
- One-time witness (OTW) and `init` assumptions; upgrade policy.
- Epoch/time-dependent logic and validator-set assumptions.
- PoC: `sui move test` with `test_scenario`; show object/coin transfer or a
  capability being used by the wrong sender.

### Soroban / Stellar
- Missing `require_auth` on the actor whose balance/allowance changes, or an
  auth tree that authorizes a broader sub-invocation than intended.
- Cross-contract reentrancy and stale storage reads/writes.
- Storage TTL/archival assumptions; entries expiring mid-flow.
- Token interface confusion (SEP-41 vs custom) and unchecked return values.
- PoC: `cargo test --features testutils` with `Env` auth mocks; show the
  unauthorized state change reverting only when the missing auth is added.

### DAML / Canton
- `signatory` / `observer` / `controller` mistakes; a choice that lets a
  non-controller change value or privacy.
- Contract-key uniqueness and archive/recreate races.
- Divulgence/privacy leaks through choice arguments or observers.
- Authorization checks that rely on party identity but not the expected role.
- PoC: `daml test` or Daml Script; show the unauthorized party can exercise or
  observe what the model says they cannot.

### L1 Go/Rust node clients
- Consensus/execution boundary: invalid state transition accepted, fork-choice
  manipulation, finality assumptions.
- P2P: malformed message DoS, peer scoring bypass, eclipse preconditions.
- Mempool: replacement/priority abuse, transaction propagation asymmetry.
- RPC/auth: unauthenticated admin namespaces, CORS, method allowlists.
- State sync / snapshot: unverified state, proof omission, restart replay.
- PoC: unit/integration test or local devnet; capture the exact message/state.

## Cross-chain
- Message replay across chains/domains, missing nonce/chainId.
- Root/validator-set verification skipped or zero-root accepted.
- Finality assumptions (source-chain reorg after mint).
- Decimals/denominations mismatch and fee-on-transfer on the destination.
- PoC: fork both sides or use a local harness; show a second mint/redeem.

## Triage for non-EVM findings
Use the same 7-Question Gate. Additionally:
- Name the exact account/object/resource and the victim's loss.
- Show the signer/authorization context in the PoC, not just the call.
- If the chain has no public fork, build a local scenario that reproduces the
  state transition; label it `LOCAL HARNESS`, not `MAINNET CONFIRMED`.
- Do not report framework/toolchain best practices without a value path.
