# SKILL: IDOR on WRITE methods (PATCH/PUT/DELETE) while GET is protected

**Skill id:** `tip/idor-on-write-methods-patchputdelete-while-get-is-protected`  
**Category:** IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880816da2aafb7382c4d27b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير apps بتحمي الـ GET بس. جرب نفس الـ ID على PATCH/PUT/DELETE. ده من أكتر الـ IDORs اللي لسه بتجيب فلوس.

## Payload / Code

```
GET /api/resource/123 → 403
PATCH /api/resource/123 → 200 (with other user session)
```

## Source

Modern IDOR Hunting 2026 + XSS Rat

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
