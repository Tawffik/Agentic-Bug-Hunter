# SKILL: IDOR via old API version (/v1/ while /v2/ is fixed)

**Skill id:** `tip/idor-via-old-api-version-v1-while-v2-is-fixed`  
**Category:** IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880817e8017e09358b88ab1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ checks الجديدة بتتضاف على /v2 أو /v3 بس. جرب /v1 أو /api/old/ بنفس الـ ID.

## Payload / Code

```
/api/v2/user/123 → protected
/api/v1/user/123 → IDOR
```

## Source

XSS Rat 2026 tip

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
