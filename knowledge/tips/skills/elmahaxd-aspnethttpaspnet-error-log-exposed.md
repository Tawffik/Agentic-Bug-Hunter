# SKILL: Elmah.axd / [ASP.NET](http://ASP.NET) error log exposed

**Skill id:** `tip/elmahaxd-aspnethttpaspnet-error-log-exposed`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081669911f0802bcc0d0e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيسرب stack traces، paths، وأحيانًا credentials أو session data.

## Payload / Code

```
[https://target.com/elmah.axd](https://target.com/elmah.axd)
[https://target.com/elmah.axd/detail?id=](https://target.com/elmah.axd/detail?id=)...
```

## Source

Classic still found + security misconfig guides

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
