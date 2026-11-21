# SKILL: BOLA via Wildcard / Special ID Values (\*, all, 0, -1, null, empty)

**Skill id:** `tip/bola-via-wildcard-special-id-values-all-0-1-null-empty`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880813e9b09d127a6e781e8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Some backends treat special values as "all objects" or skip ownership checks when the ID is not a normal UUID/integer. Replace the object ID with \*, all, any, 0, -1, null, empty string, or undefined. Also try path tricks (../users/victim, trailing / or ?). High impact when it returns mass data or allows mass modification.

## Payload / Code

```
GET /api/users/\*
GET /api/users/all
GET /api/users/0
GET /api/users/-1
GET /api/users/null
GET /api/users/

Also: id=\*, id\[\], id\[0\]=victim
```

## Source

Twitter/X @yogsec — BOLA via Wildcard & Special ID Values (Nov 2026)

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
