# SKILL: Dork (High Signal): Database dumps with real content

**Skill id:** `tip/dork-high-signal-database-dumps-with-real-content`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081cd8d5dfa08fbb007c0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيركز على dumps فيها INSERT عشان تبقى data فعلية مش أمثلة.

## Payload / Code

```
site:[target.com](http://target.com) (filetype:sql OR ext:sql) ("INSERT INTO" OR "CREATE TABLE") (password OR email OR user OR credit)
```

## Source

SecurityElites 2026 + real \$ cases

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
