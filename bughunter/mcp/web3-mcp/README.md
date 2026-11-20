# Web3 MCP Integrations

Four optional MCP servers for smart-contract work. All are **opt-in**: review the upstream
code before enabling, and only run them against contracts you are authorized to audit.

| Server | Transport | Source | Status |
|---|---|---|---|
| `foundry-mcp` | stdio (`node .../foundry-mcp/dist/index.js`) | github.com/alexbakers/foundry-mcp | npm v1.1.1 installs; published bin lacks a shebang, so invoke `node` |
| `solidity-audit-mcp` | stdio (`node dist/index.js`) | github.com/mariano-aguero/solidity-audit-mcp | **build from GitHub** |
| `evm-agent-toolkit` | stdio (`node build/mcp/index.js`) | github.com/0xendale/evm-agent-toolkit | **build from GitHub** (npm name is unpublished) |
| `solodit` | stdio (`npx -y @marchev/claudit@latest`) | github.com/marchev/claudit | npm package; needs `SOLODIT_API_KEY` |

> **Supply-chain warning (verified 2026-11-19):** the npm package named
> `solidity-audit-mcp` is a **reserved placeholder** ("Reserved name placeholder. No
> functionality."). Do **not** `npm install -g solidity-audit-mcp` or `npx` it. Clone and
> build the upstream repo instead. The repo's `package.json` exposes `solidity-audit-cli`,
> `solidity-audit-server`, and `solidity-audit-mcp` bins after `npm run build`/`npm link`.

## Prerequisites

```bash
# Foundry (forge/cast/anvil) — required by foundry-mcp and for PoCs
curl -L https://foundry.paradigm.xyz | bash && ~/.foundry/bin/foundryup

# Python analyzers used by solidity-audit-mcp
pipx install slither-analyzer solc-select crytic-compile
solc-select install 0.8.28 && solc-select use 0.8.28

# Aderyn (Rust)
cargo install aderyn

# Optional fuzzers / symbolic execution
pipx install halmos
# echidna / medusa: see bughunter/tools/external_arsenal.sh for hints

# foundry-mcp (real npm package, but the published bin has no shebang)
npm install -g foundry-mcp
node "$(npm root -g)/foundry-mcp/dist/index.js"   # starts the stdio MCP server
```

## Build evm-agent-toolkit from upstream

The npm name `@0xendale/evm-agent-toolkit` is **not published** (verified 2026-11-20).
The repository README's `npx` example is stale; build it locally:

```bash
git clone https://github.com/0xendale/evm-agent-toolkit
cd evm-agent-toolkit
npm install
npm run build
# point the MCP client at build/mcp/index.js
```

It exposes structured (Zod-validated) `slither`, `forge` gas/compile/test, `cast call --trace`,
`forge inspect storage-layout`, calldata decode, and toolchain-version tools. Prerequisites:
`slither`, `forge`, `cast`.

## Solodit MCP (claudit)

```bash
export SOLODIT_API_KEY="sk_..."   # free key: https://solodit.cyfrin.io
npx -y @marchev/claudit@latest    # stdio MCP server
```

Tools: `search_findings` (firm/tag/severity/protocol/reported/quality filters),
`get_finding`, `get_filter_options`. Use it to find paid precedent, then reproduce the
same missing check in the target; a Solodit hit is a **LEAD**, never proof.

## Build solidity-audit-mcp from upstream

```bash
git clone https://github.com/mariano-aguero/solidity-audit-mcp
cd solidity-audit-mcp
npm install
npm run build
# optional: npm link   # exposes solidity-audit-cli / solidity-audit-mcp
node dist/index.js --help
```

## OpenCode config

Copy the `mcp` block from `opencode-config.json` into your root `opencode.json`.
Replace `/ABS/PATH/...` with the real paths (for a global npm install, foundry-mcp lives at
`$(npm root -g)/foundry-mcp/dist/index.js`). Set `"enabled": false` until you have built the
server and verified it starts with `node` (not `npx`).

OpenCode format notes: `mcp` (not `mcpServers`), `command` is a single array, environment
variables go under `environment`, and `{env:VAR}` reads from the shell.

## Claude Code config

Copy `claude-config.json` into `~/.claude/mcp.json` (or project `.mcp.json`).

## What these servers are good for

- `find_contracts`, `read_contract`, `run_forge_test`, `cast_call` style tools for
  fast read/test loops against a local repo or fork.
- `analyze_contract`, `check_vulnerabilities`, `generate_invariants`, `diff_audit`,
  `explain_finding` from solidity-audit-mcp (Slither + Aderyn + SWC patterns).
- Deterministic Slither/Forge/cast JSON from `evm-agent-toolkit` — storage layout,
  call traces, calldata decode, gas, compile diagnostics, and test results without
  noisy CLI parsing.
- Solodit precedent search from `solodit` (claudit) with severity/firm/tag/protocol filters.
- Treat every output as a **LEAD**: re-run the detector, read the code, and build a
  Foundry PoC before reporting. A detector hit is not a vulnerability.

## Safety

- Do not point these servers at mainnet with funded private keys.
- Use a dedicated RPC URL and a throwaway keystore for fork tests.
- Do not let an MCP tool sign/transact on your behalf; read-only calls only unless the
  engagement explicitly allows otherwise.
- Review `package.json` / lockfiles before installing; run `npm audit` in the clone.

## Related

- `web3/36-solidity-audit-mcp.md` — full tool reference (install instructions corrected).
- `skills/web3-audit/SKILL.md` — audit methodology + `references/resources.md`.
- `bughunter/tools/external_arsenal.sh` — `forge`, `slither`, `aderyn`, `medusa`, `halmos`, `solana`, etc.