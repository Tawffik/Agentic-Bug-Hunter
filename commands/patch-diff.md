---
description: Turn a fix commit or CVE range into security hypotheses and a pre-fix PoC plan. Usage: /patch-diff <repo> [--from REF] [--to REF] [--cve CVE]
---

# /patch-diff

```bash
bash bughunter/tools/patch_diff_hunt.sh "$REPO" --from "$BASE" --to "$FIX" --cve CVE-XXXX-YYYY
```

Produces `patch-diff/report.md` with commits, changed files, security-relevant
diff lines, and six hypotheses. That is a LEAD: reproduce the pre-fix behavior
with a focused PoC before reporting.
