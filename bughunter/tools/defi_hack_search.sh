#!/usr/bin/env bash
# defi_hack_search.sh — search a local DeFiHackLabs clone for runnable exploit PoCs.
#
# DeFiHackLabs (github.com/SunWeb3Sec/DeFiHackLabs) is a large corpus of real
# DeFi hacks reproduced with Foundry. Clone it once, then search by protocol,
# function, token, or bug-class keyword. Results are LEADS: read the PoC, map
# the root cause, and prove the same missing check exists in your target.
#
# Usage:
#   ./defi_hack_search.sh <term> [--dir DIR] [--limit N] [--all]
#   ./defi_hack_search.sh --help
#
# Env: DEFI_HACKLABS_DIR  default: ~/.cache/defi-hacklabs
set -euo pipefail

DIR="${DEFI_HACKLABS_DIR:-$HOME/.cache/defi-hacklabs}"
LIMIT=20
TERM=""
ALL=0

usage() {
  cat <<'EOF'
Usage: defi_hack_search.sh <term> [--dir DIR] [--limit N] [--all]

Search a local DeFiHackLabs clone for exploit PoCs matching <term>.
  --dir DIR    clone path (default: $DEFI_HACKLABS_DIR or ~/.cache/defi-hacklabs)
  --limit N    max matches (default: 20)
  --all        print every matching line, not just the first per file

Clone once (large, shallow is enough):
  git clone --depth 1 https://github.com/SunWeb3Sec/DeFiHackLabs "$HOME/.cache/defi-hacklabs"

Safe for authorized research only. A matched PoC is precedent, not proof.
EOF
}

need_arg() {
  [ $# -ge 2 ] || { echo "error: $1 needs a value" >&2; exit 2; }
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --dir) need_arg "$@"; DIR="$2"; shift 2 ;;
    --limit) need_arg "$@"; LIMIT="$2"; shift 2 ;;
    --all) ALL=1; shift ;;
    --) shift; break ;;
    -*) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *) TERM="${TERM:-$1}"; shift ;;
  esac
done

if [ -z "$TERM" ]; then
  usage >&2
  exit 2
fi

if [ ! -d "$DIR" ]; then
  cat >&2 <<EOF
[!] DeFiHackLabs clone not found: $DIR
    git clone --depth 1 https://github.com/SunWeb3Sec/DeFiHackLabs "$DIR"
    # or pass --dir /path/to/DeFiHackLabs
EOF
  exit 1
fi

ROOTS=()
for p in "$DIR/src" "$DIR/past" "$DIR/academy" "$DIR/README.md"; do
  [ -e "$p" ] && ROOTS+=("$p")
done
if [ ${#ROOTS[@]} -eq 0 ]; then
  echo "[!] no src/, past/, or README.md under $DIR" >&2
  exit 1
fi

if command -v rg >/dev/null 2>&1; then
  SEARCH=(rg -n -i --no-heading --color never --glob '*.sol' --glob '*.md')
else
  SEARCH=(grep -RniI --include='*.sol' --include='*.md')
fi

mapfile -t MATCHES < <("${SEARCH[@]}" -- "$TERM" "${ROOTS[@]}" 2>/dev/null | head -n "$LIMIT" || true)

if [ ${#MATCHES[@]} -eq 0 ]; then
  echo "No matches for '$TERM' in $DIR"
  exit 0
fi

echo "# DeFiHackLabs matches: $TERM"
echo "# root: $DIR"
echo "# (LEAD-only: verify the root cause on your target; do not submit precedent)"
echo
if [ "$ALL" -eq 1 ]; then
  printf '%s\n' "${MATCHES[@]}"
else
  printf '%s\n' "${MATCHES[@]}" | awk -F: '!seen[$1]++ {print}'
  echo
  echo "# pass --all to print every matching line"
fi
