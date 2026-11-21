# SKILL: Advanced Dork: SQL dumps with real data

**Skill id:** `tip/advanced-dork-sql-dumps-with-real-data`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880810da9b2d33ecad8ace1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيركز على dumps اللي فيها INSERT أو CREATE TABLE عشان تبقى data حقيقية مش أمثلة.

## Payload / Code

```
site:[target.com](http://target.com) filetype:sql ("INSERT INTO" OR "CREATE TABLE") (password OR email OR credit)
```

## Source

Hacklido + Medium 2025-2026

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
