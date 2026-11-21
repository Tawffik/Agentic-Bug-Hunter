# SKILL: GitHub Dork: DB connection strings

**Skill id:** `tip/github-dork-db-connection-strings`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081fba8add48a7ac83d00  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

mongodb+srv / postgres / mysql غالبًا فيها credentials كاملة.

## Payload / Code

```
org:TARGET ("mongodb+srv://" OR "postgres://" OR "postgresql://" OR "mysql://")
```

## Source

Intigriti + real findings

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
