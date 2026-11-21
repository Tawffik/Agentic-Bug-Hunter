# SKILL: 403/401 host → [archive.org](http://archive.org) old snapshots still have secrets

**Skill id:** `tip/403401-host-archiveorghttparchiveorg-old-snapshots-still-have-secrets`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081f08651f12e21b8ca9d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لما تلاقي host بيرجع 401/403 أو basic auth، روح لـ [archive.org](http://archive.org) وشوف الـ historical snapshots. أحيانًا الـ old versions فيها API keys أو unprotected content لسه موجود.

## Payload / Code

```
[https://web.archive.org/web/](https://web.archive.org/web/)/[https://locked-host.target.com/](https://locked-host.target.com/)
```

## Source

Book of BugBounty Tips + multiple hunters

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
