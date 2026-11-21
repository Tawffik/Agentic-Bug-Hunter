# SKILL: BOLA / IDOR via Batch & Bulk ID Mixing

**Skill id:** `tip/bola-idor-via-batch-bulk-id-mixing`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081a9986ed665d810b9a2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Many APIs expose batch/bulk endpoints that accept arrays of object IDs (ids\[\], JSON array of objects, /api/batch). Authorization is often checked only on the first ID or skipped per-item. Mix your own IDs with a victim ID in the same request; also try duplicate keys, partial-failure responses that leak existence, and array stuffing. If the server processes the victim object, you have scalable BOLA.

## Payload / Code

```
POST /api/batch
\{"ids": \["your-id", "victim-id"\]\}

or
ids\[\]=your-id&ids\[\]=victim-id

or mixed objects:
\[\{"id":"your-id"\}, \{"id":"victim-id"\}\]
```

## Source

Twitter/X @yogsec — BOLA via Batch/Bulk Request ID Mixing (Nov 2026)

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
