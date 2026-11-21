# SKILL: Shodan Dork: Favicon hash pivot

**Skill id:** `tip/shodan-dork-favicon-hash-pivot`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e8808129a9e0f7e8c03e89dc  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

خد الـ favicon hash من FOFA أو الموقع، ودور بيه على كل الـ assets المشابهة.

## Payload / Code

```
http.favicon.hash:HASH\_VALUE
```

## Source

FaviconHasher + your Dorks page

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
