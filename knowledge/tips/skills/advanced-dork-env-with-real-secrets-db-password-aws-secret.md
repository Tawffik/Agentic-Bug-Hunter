# SKILL: Advanced Dork: .env with real secrets (DB\_PASSWORD / AWS\_SECRET)

**Skill id:** `tip/advanced-dork-env-with-real-secrets-db-password-aws-secret`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081a18c82f71753bd0e9f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ابحث عن .env اللي فيه علامات secrets حقيقية مش مجرد أسماء. دي بتجيب نتائج عالية الجودة.

## Payload / Code

```
site:[target.com](http://target.com) (ext:env OR inurl:.env) ("DB\_PASSWORD" OR "AWS\_SECRET\_ACCESS\_KEY" OR "SECRET\_KEY" OR "APP\_KEY")
```

## Source

[dorksearch.com](http://dorksearch.com) + multiple 2025-2026 guides

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
