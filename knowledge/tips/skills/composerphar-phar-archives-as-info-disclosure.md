# SKILL: composer.phar / phar archives as Info Disclosure

**Skill id:** `tip/composerphar-phar-archives-as-info-disclosure`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ceb812d2be91b294c4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أضف /composer.phar لقوائم الـ content discovery. لو موجود و readable، استخدم pharfiletool لاستخراج المحتوى (كود أو metadata).

## Payload / Code

```
[https://target.com/composer.phar](https://target.com/composer.phar)
# ثم pharfiletool extract
```

## Source

nooh zidan tip + hunters

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
