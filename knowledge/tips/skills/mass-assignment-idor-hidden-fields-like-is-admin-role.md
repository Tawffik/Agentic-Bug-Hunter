# SKILL: Mass Assignment + IDOR (hidden fields like is\_admin / role)

**Skill id:** `tip/mass-assignment-idor-hidden-fields-like-is-admin-role`  
**Category:** IDOR, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081fa98f5d971e005f1f2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في update profile أو object، ابعت fields مش ظاهرة في الـ frontend (is\_admin, role, permissions, owner\_id).

## Payload / Code

```
PATCH /api/profile
\{"username":"x", "is\_admin":true, "role":"admin"\}
```

## Source

Beyond BOLA 2025 + Modern IDOR 2026

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
