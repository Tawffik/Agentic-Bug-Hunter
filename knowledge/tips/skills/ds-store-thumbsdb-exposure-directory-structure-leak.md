# SKILL: .DS\_Store + Thumbs.db exposure → directory structure leak

**Skill id:** `tip/ds-store-thumbsdb-exposure-directory-structure-leak`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081d2ad12ca0ca49d6559  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ملفات macOS/Windows hidden بتتساب على السيرفر. .DS\_Store بيكشف أسماء الملفات والمجلدات، Thumbs.db نفس الفكرة. مفيد جداً لما تلاقي directory listing مقفول.

## Payload / Code

```
[https://target.com/.DS\_Store](https://target.com/.DS_Store)
[https://target.com/Thumbs.db](https://target.com/Thumbs.db)
# استخدم dsstore parser بعد التحميل
```

## Source

Classic overlooked recon (still pays when combined with sensitive paths)

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
