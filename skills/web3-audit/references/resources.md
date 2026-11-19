# Web3 Audit — Best Resources & Toolchain

> Curated, high-signal sources. Read the pattern, then reproduce it on the current in-scope code.
> A detector hit, audit finding, or past exploit is a **LEAD** — not a vulnerability in your target.

---

## 1. Finding databases / precedent

| Resource | Use it for |
|---|---|
| **Solodit** — https://solodit.cyfrin.io | Search real audit findings by protocol/pattern; best for "has this exact bug been paid?" |
| **Immunefi** — https://immunefi.com | Program rules, severity classification, disclosed reports, payout precedent |
| **Rekt News** — https://rekt.news | Postmortems; map a real loss to the root-cause class |
| **DeFiHackLabs** — https://github.com/SunWeb3Sec/DeFiHackLabs | Runnable Foundry PoCs for real hacks; fastest way to learn an exploit shape |
| **DeFiVulnLabs** — https://github.com/SunWeb3Sec/DeFiVulnLabs | Small vulnerable examples per class |
| **SWC Registry** — https://swcregistry.io | CWE-style mapping for reports |
| **OWASP Smart Contract Top 10** — https://owasp.org/www-project-smart-contract-top-10/ | Coverage checklist / report framing |
| **Smart Contract Weakness Classification** (repo) | Detector mapping and severity hints |

Use Solodit to find **2–3 analogous** findings, then compare the vulnerable code shape — not just the
category. If your target's code does not have the same missing check/path, you do not have the bug.

## 2. Methodology / secure-engineering references

| Resource | Use it for |
|---|---|
| **Trail of Bits — Building Secure Contracts** https://github.com/crytic/building-secure-contracts | Per-chain checklists, invariants, Echidna/Medusa guidance |
| **ConsenSys Smart Contract Best Practices** https://consensys.github.io/smart-contract-best-practices/ | Known pitfalls, upgradeability, token integration |
| **Cyfrin** https://www.cyfrin.io/ + **Updraft** | Audit reasoning, DeFi patterns, report examples |
| **Secureum** https://secureum.xyz | Structured audit curriculum + quizzes |
| **Foundry Book** https://book.getfoundry.sh | forge/cast/anvil, cheatcodes, forks, invariant testing |
| **Ethereum EIPs** https://eips.ethereum.org | Exact token/standard behavior (ERC20/4626/4337/7702) |
| **Solana — Sealevel Attacks** https://github.com/coral-xyz/sealevel-attacks | Solana-specific bug classes with examples |
| **Anchor Book** https://www.anchor-lang.com | Account validation, constraints, CPIs |
| **Solana docs** https://solana.com/docs | Runtime, PDAs, token program, compute budget |

## 3. Local toolchain

Installed/registered via `./install_tools.sh --with-web3` and
`bughunter/tools/external_arsenal.sh`:

| Tool | Role |
|---|---|
| `forge`, `cast`, `anvil` | build/test/fork/inspect; PoC + invariant tests |
| `slither` | static analysis, data-flow, detectors |
| `solc-select` | pin compiler versions per target |
| `crytic-compile` | compile integration for Slither/Echidna |
| `aderyn` | **retired upstream (2026)** — existing installs only; use Slither + Medusa/Halmos |
| `echidna` | property-based fuzzing |
| `medusa` | Go fuzzer (alternative to Echidna) |
| `halmos` | symbolic execution for Solidity |
| `myth` (Mythril) | symbolic execution / concolic |
| `surya` | call graphs, inheritance, function maps |
| `heimdall` | decompile / CFG for bytecode |
| `wake` | Python testing/analysis framework |
| `solhint` | lint / best-practice checks |
| `solana`, `anchor`, `surfpool` | Solana build/test/local validator |
| `foundry-mcp`, `solidity-audit-mcp` | MCP servers (see `bughunter/mcp/web3-mcp/`) |

### Quick commands

```bash
# Compile + tests + gas
forge build
forge test -vvv
forge test --gas-report
forge coverage --report summary

# Fork a real chain at a block
forge test --fork-url "$RPC_URL" --fork-block-number 20000000 -vvvv

# Static analysis
slither . --config-file slither.config.json
# aderyn .   # retired upstream; only if already installed
surya inheritance .
surya graph contracts/*.sol | dot -Tpng > graph.png

# Fuzzing / symbolic
echidna-test . --contract Vault --config echidna.yaml
medusa fuzz
halmos --contract Vault

# Bytecode
heimdall decompile 0x... --output out
```

## 4. Bug-class → resource map

| Class | Start here |
|---|---|
| Accounting desync | Solodit "accounting", DeFiHackLabs, protocol invariant tests |
| Access control | SWC-105/106, sibling-function rule in `SKILL.md` |
| Incomplete path | function-family diff, DeFiHackLabs PoCs |
| Off-by-one | boundary checklist, fuzz/invariant tests |
| Oracle / price | Chainlink/Pyth docs, "donation attack", TWAP length |
| ERC4626 | EIP-4626, donation/inflation attack writeups |
| Reentrancy | SWC-107, checks-effects-interactions, ERC777/721 callbacks |
| Flash loan | DeFiHackLabs, oracle manipulation PoCs |
| Signature replay | EIP-712, nonce/chainId/domain separator |
| Proxy/upgrade | OZ upgrades docs, storage layout, initializer front-run |
| Solana | Sealevel Attacks, Anchor constraints, PDA/signers |

## 5. Report-ready references

- Map the finding to **SWC** and **OWASP SC Top 10** for credibility.
- Cite the **spec** (EIP/ERC/Anchor) when behavior violates it.
- Include a **Foundry PoC** (`forge test --match-test ... -vvvv`) and the exact fork block.
- Quantify impact: funds at risk, repeatability, prerequisites, whether it is atomic.
- If using a past exploit as precedent, cite it but show your own reproduction.

## 6. What not to use

- Unverified "audit checklist" repos with no PoC or code reference.
- AI-generated finding lists without a runnable reproduction.
- `npm install solidity-audit-mcp` — reserved placeholder package (supply-chain risk).
- Exploit code against mainnet contracts you do not own or have authorization to test.