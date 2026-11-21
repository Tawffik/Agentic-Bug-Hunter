# SKILL: Laravel storage/logs or error.log / debug.log exposed

**Skill id:** `tip/laravel-storagelogs-or-errorlog-debuglog-exposed`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880818bbb17cf25f879b52d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ logs بتحتوي stack traces، paths، وأحيانًا tokens أو PII. جرب /storage/logs/laravel.log أو /error.log.

## Payload / Code

```
[https://target.com/storage/logs/laravel.log](https://target.com/storage/logs/laravel.log)
[https://target.com/error.log](https://target.com/error.log)
[https://target.com/debug.log](https://target.com/debug.log)
```

## Source

Common in PHP frameworks

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
