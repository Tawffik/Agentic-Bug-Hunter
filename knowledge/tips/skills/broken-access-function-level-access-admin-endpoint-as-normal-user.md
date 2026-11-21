# SKILL: Broken Access: function-level (access admin endpoint as normal user)

**Skill id:** `tip/broken-access-function-level-access-admin-endpoint-as-normal-user`  
**Category:** Auth Bypass, IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880813ca8e8d14ce6df9db1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مش IDOR object، ده endpoint كامل. جرب /admin/, /api/internal/, /manage/\* بسيشن يوزر عادي.

## Payload / Code

```
As low-priv user: GET /api/admin/users or /internal/config
```

## Source

Broken Access Control 2026 blueprint

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
