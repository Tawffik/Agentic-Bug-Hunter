# SKILL: Second-order IDOR (create → background process → leak)

**Skill id:** `tip/second-order-idor-create-background-process-leak`  
**Category:** IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081ce9506edbe71573fc9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اعمل resource، غيّر reference مخفي، استنى background job، شوف النتيجة في مكان تاني (email, export, notification).

## Payload / Code

```
Create → modify hidden ID → wait for async process → check other user view
```

## Source

Modern IDOR Hunting 2026

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
