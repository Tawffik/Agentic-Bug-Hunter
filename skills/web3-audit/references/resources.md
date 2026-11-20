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
| **DeFiHackLabs** — https://github.com/SunWeb3Sec/DeFiHackLabs | Runnable Foundry PoCs for real hacks; fastest way to learn an exploit shape. Search locally with `bughunter/tools/defi_hack_search.sh` |
| **DeFiVulnLabs** — https://github.com/SunWeb3Sec/DeFiVulnLabs | Small vulnerable examples per class |
| **Cyfrin audit reports** — https://github.com/Cyfrin/cyfrin-audit-reports | Real report corpus; use it to compare a candidate's wording, severity, and finding shape against paid precedent |
| **Solodit MCP (claudit)** — https://github.com/marchev/claudit | Search 20K+ Solodit findings from the agent; `search_findings`, `get_finding`, `get_filter_options` |
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
| **Pashov fizz** https://github.com/pashov/skills/tree/main/fizz | Stateful Echidna/Medusa suite generation; mirrored in `skills/web3-fuzz/` |
| **Pashov x-ray** https://github.com/pashov/skills/tree/main/x-ray | Pre-audit threat model, entry points, invariants, git-history risk |
| **Trail of Bits skills** https://github.com/trailofbits/skills | Contract audit, variant analysis, entry-point plugins |
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
| `echidna` | property-based fuzzing (installed by `install_tools.sh --with-web3`; env `ECHIDNA_VERSION` overrides the pinned release) |
| `medusa` | Go fuzzer (alternative to Echidna) |
| `halmos` | symbolic execution for Solidity |
| `myth` (Mythril) | symbolic execution / concolic |
| `surya` | call graphs, inheritance, function maps |
| `heimdall` | decompile / CFG for bytecode |
| `wake` | Python testing/analysis framework |
| `solhint` | lint / best-practice checks |
| `solana`, `anchor`, `surfpool` | Solana build/test/local validator |
| `foundry-mcp`, `solidity-audit-mcp` | MCP servers (see `bughunter/mcp/web3-mcp/`) |
| `evm-agent-toolkit` | source-built MCP: structured Slither/Forge/cast, storage layout, traces, calldata decode |
| `claudit` | Solodit MCP; set `SOLODIT_API_KEY` |
| `web3-fuzz` | stateful fuzz-suite generation (Echidna/Medusa/Foundry) |
| `defi_hack_search.sh` | search a local DeFiHackLabs clone for runnable PoCs |
| `chain_audit_env.sh` | detect EVM/Solana/Move/Soroban/DAML toolchain + commands |
| `xray_git_security.py` | git-history risk ranking for pre-audit x-ray (`--json`) |

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
| Multichain | `web3/13-multichain-audit.md` — Solana, Aptos/Sui Move, Soroban, DAML, L1 clients |
| Validation | `references/validation-gates.md` (4 gates + confidence) |

## 5. AI-agent and benchmark sources

| Resource | Use it for |
|---|---|
| **Hound** https://github.com/scabench-org/hound | Knowledge-graph audit agent; belief/hypothesis tracking; optional external CLI (see arsenal) |
| **Plamen** https://github.com/PlamenTSV/plamen | Multi-chain audit orchestration; its language-toolchain registry informed `web3/13-multichain-audit.md` |
| **AuditCode** https://github.com/itsdarktoday/auditcode | Multi-agent audit harness; its 4-gate web3 filter informed `validation-gates.md` |
| **EVMbench** https://github.com/paradigmxyz/evmbench | Agent benchmark for finding/exploiting contract bugs |
| **SCONE-bench** https://github.com/safety-research/SCONE-bench | 405-contract exploit benchmark built from DeFiHackLabs |
| **ScaBench** https://github.com/scabench-org/scabench | 31 projects / 555 audit vulnerabilities; measure coverage, not vibes |

## 6. Report-ready references

- Map the finding to **SWC** and **OWASP SC Top 10** for credibility.
- Cite the **spec** (EIP/ERC/Anchor) when behavior violates it.
- Include a **Foundry PoC** (`forge test --match-test ... -vvvv`) and the exact fork block.
- Quantify impact: funds at risk, repeatability, prerequisites, whether it is atomic.
- If using a past exploit as precedent, cite it but show your own reproduction.

## 7. What not to use

- Unverified "audit checklist" repos with no PoC or code reference.
- AI-generated finding lists without a runnable reproduction.
- `npm install solidity-audit-mcp` — reserved placeholder package (supply-chain risk).
- Exploit code against mainnet contracts you do not own or have authorization to test.