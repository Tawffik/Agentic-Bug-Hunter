#!/usr/bin/env bash
# Patch-diff hunt — turn a fix commit/CVE range into security hypotheses.
#
# Usage:
#   ./patch_diff_hunt.sh <repo> [--from REF] [--to REF] [--out DIR] [--cve CVE-XXXX-YYYY]
#
# Defaults: --to HEAD, --from HEAD~1, --out ./patch-diff
# Output: report.md (diff, changed files, security keywords, commit messages)
#         diff.patch (raw unified diff)
#
# Read-only. The script does not build, run, or modify the target.
set -euo pipefail

REPO=""
FROM="HEAD~1"
TO="HEAD"
OUT="patch-diff"
CVE=""
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    --from) FROM="$2"; shift 2 ;;
    --to) TO="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --cve) CVE="$2"; shift 2 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) REPO="${REPO:-$1}"; shift ;;
  esac
done

[ -n "$REPO" ] || { echo "usage: $0 <repo> [--from REF] [--to REF] [--out DIR] [--cve CVE]" >&2; exit 2; }
git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repo: $REPO" >&2; exit 2; }
git -C "$REPO" rev-parse "$FROM" >/dev/null 2>&1 || { echo "bad --from: $FROM" >&2; exit 2; }
git -C "$REPO" rev-parse "$TO" >/dev/null 2>&1 || { echo "bad --to: $TO" >&2; exit 2; }

[ "$OUT" = "patch-diff" ] && OUT="$REPO/patch-diff"
mkdir -p "$OUT"
DIFF="$OUT/diff.patch"
REPORT="$OUT/report.md"
git -C "$REPO" diff --unified=5 "$FROM..$TO" > "$DIFF"

{
  echo "# Patch-diff hunt — $REPO"
  echo
  echo "- Range: \`$FROM..$TO\`"
  [ -n "$CVE" ] && echo "- CVE: \`$CVE\`"
  echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## Commits"
  echo
  echo '```text'
  git -C "$REPO" log --oneline "$FROM..$TO" | head -40
  echo '```'
  echo
  echo "## Changed files"
  echo
  echo '```text'
  git -C "$REPO" diff --stat "$FROM..$TO"
  echo '```'
  echo
  echo "## Security-relevant diff lines"
  echo
  echo '```diff'
  grep -nE '^[+-][^+-].*(require|revert|assert|onlyOwner|onlyRole|onlyAdmin|nonReentrant|initializer|delegatecall|ecrecover|ECDSA|signature|nonce|balance|totalSupply|totalAssets|exchangeRate|transfer|transferFrom|mint|burn|oracle|price|liquidat|upgrade|slot|owner)' "$DIFF" | head -200 || true
  echo '```'
  echo
  echo "## Hypotheses to test"
  echo
  cat <<'DOC'
1. What guard/check did the fix add or remove? Can the old path still be reached?
2. Which sibling function/caller still lacks the same check? (the missing-modifier rule)
3. Which state variable's update was moved/added? Is there an early return or alternate branch that skips it?
4. Does the fix cover every token/decimals/address type and every caller in the protocol?
5. Can the pre-fix behavior be reproduced on a local fork with the smallest possible PoC?
6. Is the vulnerable version still deployed in scope? Map commit/tag -> deployed bytecode.
DOC
  echo
  echo "## Raw diff"
  echo
  echo '```diff'
  head -400 "$DIFF"
  echo '```'
  echo
  echo "_Truncated raw diff in report; full diff: \`$DIFF\`._"
} > "$REPORT"

echo "[+] report: $REPORT"
echo "[+] diff:   $DIFF"
grep -cE '^[+-]' "$DIFF" | xargs echo "[+] changed lines:" || true
