# SKILL: Wayback archived files when live path returns 404 or Access Denied

**Skill id:** `tip/wayback-archived-files-when-live-path-returns-404-or-access-denied`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808154b17be60e4f5e9e4e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Sensitive files (.xls, .csv, dumps) may be removed or blocked on the live host (404 / Access Denied) while Wayback still has a fully readable archived copy. Use historical URLs for authorized disclosure research only; do not mass-download PII beyond minimal evidence.

## Payload / Code

```
1) Collect URLs (waybackurls / gau / CDX)
2) Filter extensions: xls, xlsx, csv, sql, zip, pdf
3) If live = 404 or Access Denied → open archived version
4) Confirm sensitivity + in-scope asset before reporting

CDX idea:
[https://web.archive.org/cdx/search/cdx?url=](https://web.archive.org/cdx/search/cdx?url=).[target.com/](http://target.com/)&fl=original&collapse=urlkey

Filter for .xls / .csv / .sql
```

## Source

Mohamed Ahmed — Wayback Machine method (@coffinxp7)

## Agent execution contract

1. Confirm asset is in authorized scope.
2. Baseline with an account/object you control.
3. Apply **one** mutation from the payload at a time.
4. Discriminate benign explanations (cache, public data, UI-only).
5. Classify as **LEAD** until unauthorized consequence is proven.
6. Stop if real third-party data appears beyond minimal evidence.
7. Hand off to report template only after validation checklist passes.

---
_Synced from Notion Bug Bounty Tips and Tricks · agent skill ready._
