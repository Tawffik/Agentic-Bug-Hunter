#!/usr/bin/env bash
# chain_audit_env.sh — detect a Web3 project's chain/toolchain and print the
# exact build/test/fuzz commands plus missing tools.
#
# Usage: ./chain_audit_env.sh <project-dir> [--json]
#        ./chain_audit_env.sh --help
set -euo pipefail

JSON=0
ROOT=""

usage() {
  cat <<'EOF'
Usage: chain_audit_env.sh <project-dir> [--json]

Detects Foundry/Hardhat (EVM), Anchor (Solana), Aptos/Sui Move, Soroban,
and DAML projects. Prints build/test/fuzz commands and missing tools.
Read-only: never builds or executes a target command.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --json) JSON=1; shift ;;
    -*) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *) ROOT="${ROOT:-$1}"; shift ;;
  esac
done

[ -n "$ROOT" ] || { usage >&2; exit 2; }
[ -d "$ROOT" ] || { echo "error: not a directory: $ROOT" >&2; exit 2; }

has() { command -v "$1" >/dev/null 2>&1; }
contains() { grep -qiE "$1" "$2" 2>/dev/null; }

CHAINS=()
add() { CHAINS+=("$1"); }

if [ -f "$ROOT/foundry.toml" ]; then
  add "evm-foundry"
elif [ -f "$ROOT/hardhat.config.ts" ] || [ -f "$ROOT/hardhat.config.js" ] \
  || { [ -f "$ROOT/package.json" ] && contains 'hardhat' "$ROOT/package.json"; }; then
  add "evm-hardhat"
fi

[ -f "$ROOT/Anchor.toml" ] && add "solana-anchor"

if [ -f "$ROOT/Move.toml" ]; then
  if contains 'sui' "$ROOT/Move.toml"; then add "sui-move"; else add "aptos-move"; fi
fi

if [ -f "$ROOT/Cargo.toml" ] && contains 'soroban-sdk' "$ROOT/Cargo.toml"; then
  add "soroban"
fi

[ -f "$ROOT/daml.yaml" ] && add "daml"

if [ ${#CHAINS[@]} -eq 0 ]; then
  add "unknown"
fi

TOOLS=(forge cast anvil medusa echidna npx node anchor aptos sui stellar cargo daml)
have_json=""
for t in "${TOOLS[@]}"; do
  if has "$t"; then have_json+="\"$t\":true,"; else have_json+="\"$t\":false,"; fi
done
have_json="${have_json%,}"

case "${CHAINS[0]}" in
  evm-foundry)
    BUILD="forge build"; TEST="forge test -vvv"; FUZZ="medusa fuzz  # or: echidna . --contract FuzzTester --config echidna.yaml" ;;
  evm-hardhat)
    BUILD="npx hardhat compile"; TEST="npx hardhat test"; FUZZ="npx hardhat test --grep fuzz" ;;
  solana-anchor)
    BUILD="anchor build"; TEST="anchor test"; FUZZ="trident fuzz run fuzz_0  # or cargo test proptest_*" ;;
  aptos-move)
    BUILD="aptos move compile"; TEST="aptos move test"; FUZZ="aptos move test --filter test_" ;;
  sui-move)
    BUILD="sui move build"; TEST="sui move test"; FUZZ="sui move test --rand-num-iters 256" ;;
  soroban)
    BUILD="stellar contract build"; TEST="cargo test --features testutils"; FUZZ="cargo +nightly fuzz run fuzz_target" ;;
  daml)
    BUILD="daml build"; TEST="daml test"; FUZZ="daml test  # property tests via Daml Script" ;;
  *)
    BUILD="unknown"; TEST="unknown"; FUZZ="unknown" ;;
esac

if [ "$JSON" -eq 1 ]; then
  printf '{"root":"%s","chains":[' "$ROOT"
  for i in "${!CHAINS[@]}"; do
    [ "$i" -gt 0 ] && printf ','
    printf '"%s"' "${CHAINS[$i]}"
  done
  printf '],"build":"%s","test":"%s","fuzz":"%s","tools":{%s}}\n' "$BUILD" "$TEST" "$FUZZ" "$have_json"
  exit 0
fi

echo "Project: $ROOT"
echo "Detected: ${CHAINS[*]}"
echo
echo "Build: $BUILD"
echo "Test:  $TEST"
echo "Fuzz:  $FUZZ"
echo
echo "Toolchain:"
for t in "${TOOLS[@]}"; do
  if has "$t"; then printf '  [ok]      %s\n' "$t"; else printf '  [missing] %s\n' "$t"; fi
done
echo
echo "Next: read web3/13-multichain-audit.md for chain-specific bug classes,"
echo "      then prove each candidate with a target-local PoC."
