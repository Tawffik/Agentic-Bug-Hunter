# SKILL: Dork (High Signal): Index of with sensitive names

**Skill id:** `tip/dork-high-signal-index-of-with-sensitive-names`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081a0b455daa0cdc5b9e2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب open directories اللي فيها ملفات حساسة.

## Payload / Code

```
site:[target.com](http://target.com) intitle:"index of" (.env OR .git OR backup OR config OR admin OR private OR sql OR dump OR credentials)
```

## Source

Classic still paying + 2026 lists

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
