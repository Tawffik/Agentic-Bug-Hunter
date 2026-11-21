# SKILL: Wayback archived sensitive files when live returns 404/Access Denied

**Skill id:** `tip/wayback-archived-sensitive-files-when-live-returns-404access-denied`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081c19b1cd12f2384f3d6  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الملف اتشال من الـ live أو بقى 403/404، بس لسه موجود في Wayback أو URLScan. دور على .xls, .csv, dumps, configs قديمة.

## Payload / Code

```
[web.archive.org/cdx/search/cdx?url=](http://web.archive.org/cdx/search/cdx?url=).[target.com/](http://target.com/)&fl=original&collapse=urlkey \| grep -E '.(xls\|csv\|sql\|bak\|env)'
```

## Source

Multiple hunters + existing Notion entry enhancement

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
