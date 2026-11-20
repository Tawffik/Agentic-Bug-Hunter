# Pre-audit x-ray — protocol map before hunting

Adapted from Pashov Audit Group's MIT-licensed `x-ray` skill
(https://github.com/pashov/skills/tree/main/x-ray). Run this before reading
individual functions; it prevents "random grep hunting" and produces the
invariants that later validation depends on.

## 1. Enumerate and measure

```bash
# Source files, nSLOC, tests, docs, git stats
bash bughunter/tools/chain_audit_env.sh <repo>
find <src> -name '*.sol' -not -path '*/test/*' -not -path '*/lib/*' | xargs wc -l
forge coverage --report summary || true
```

Record: compiler versions, proxy pattern, upgrade authority, external
dependencies, test coverage, and nSLOC per core contract.

## 2. Git-history risk (unique signal)

```bash
python3 bughunter/tools/xray_git_security.py --repo <repo> --src-dir <src> \
  --json /tmp/git-security.json
```

Adapted from pashov/x-ray. It ranks commits by security intent + structural diff
(added/removed guards, access modifiers, transfer/signature/accounting edits),
dangerous-area churn, late changes, forked dependencies, and dev patterns.
Read the top `fix_candidates` and `dangerous_area_changes` — a recent "fix"
often marks the exact area to re-test.

## 3. Entry points and roles

| Map | Questions |
|---|---|
| Public/external functions | Which move value, mint/burn shares, change debt, or set authority? |
| Payable functions | Where can ETH enter, and is `msg.value` used once? |
| Privileged functions | owner/role/keeper/liquidator; is the role's power documented? |
| Callbacks | ERC721/1155/777 hooks, flash-loan callbacks, whitelisting callbacks |
| Upgrade paths | initializer, `_disableInitializers`, storage gaps, module pointers |

## 4. Threat model by protocol type

- **Vault/ERC4626** — share inflation, donation, rounding direction, fee-on-transfer,
  reentrancy on `totalAssets`, oracle share price.
- **Lending** — collateral factor, liquidation bonus, bad debt, oracle staleness,
  interest index, cross-market isolation.
- **AMM/DEX** — spot-price oracle, `sync`/`skim`, LP token pricing, fee-on-transfer,
  first-LP share, sandwich/MEV.
- **Staking** — reward index, cooldown, slashing, delegation, reward dilution.
- **Bridge** — message replay, root/validator-set verification, finality, decimals,
  destination mint authority.
- **Governance** — flash-loaned voting, timelock, quorum, proposal execution.

## 5. Invariants (carry into fuzzing)

Write them as equations, not prose:

```text
totalAssets >= sum(user assets) - known bad debt
sum(shares) == totalSupply
exchangeRate is monotonic except documented fee/slashing paths
sum(operator earnings) + cluster balances <= contract ETH balance
only role X can change parameter P
```

These become `property_*` functions in `skills/web3-fuzz/` and the assertions in
your Foundry PoC. If a candidate does not violate an invariant or a documented
promise, it is a smell, not a finding.

## 6. Test and docs quality

- Do tests cover failure paths, access control, and multi-actor flows?
- Does NatSpec claim a guarantee the code does not enforce? (`@notice onlyOwner`,
  "cannot be zero", "non-reentrant")
- Do docs/specs describe a different formula or ordering than the code?
- Is the deployed bytecode source-verified and pinned to a commit?

## 7. Output

Write `x-ray.md` next to the target repo (or in the hunt workspace) with:
overview, architecture diagram, roles, entry points, invariants, external
dependencies, git-risk findings, test gaps, and a ranked hypothesis list.
Every hypothesis gets a kill condition before you start reading code.
