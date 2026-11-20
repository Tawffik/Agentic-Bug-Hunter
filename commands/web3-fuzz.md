---
description: Generate and run a stateful Echidna/Medusa/Foundry fuzz suite for a Solidity project, then convert counterexamples into Foundry PoCs. Usage: /web3-fuzz <project-path>
---

# /web3-fuzz

Load the `web3-fuzz` skill and generate a stateful invariant suite for the target
project. This is a local-code workflow; never send mainnet transactions.

## Usage

```
/web3-fuzz ./protocol
/web3-fuzz /path/to/foundry-or-hardhat-repo
```

## Execute

1. Load `skills/web3-fuzz/SKILL.md`.
2. Run `bash bughunter/tools/chain_audit_env.sh <project>`.
3. Verify `forge --version`, `medusa --version`, and `echidna --version`
   (`./install_tools.sh --with-web3` installs the stack).
4. Follow the skill steps: ABI extract → entry-point selection → scaffold →
   setup/handlers → coverage loop → invariants → Medusa/Echidna → triage.
5. For each violation, reproduce the minimized sequence in a standalone Foundry
   test (`forge test --match-test ... -vvvv`) and apply
   `skills/web3-audit/references/validation-gates.md`.
6. Report only `CONFIRMED` findings; everything else is `LEAD — NOT EXECUTED`.

Output stays under `<project>/test/fizz/` and `<project>/fizz_data/`.
