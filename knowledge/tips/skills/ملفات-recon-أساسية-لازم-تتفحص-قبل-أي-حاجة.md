# SKILL: ملفات Recon أساسية لازم تتفحص قبل أي حاجة

**Skill id:** `tip/ملفات-recon-أساسية-لازم-تتفحص-قبل-أي-حاجة`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081a6ad5af341d9f695e2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

قبل ما تشغّل عشرات أدوات الريكون، الملفات دي بتكشف معلومات قيّمة عن بنية الأبلكيشن، الـ endpoints، والمصادر الحساسة بسرعة وبدون أي أدوات معقدة.

## Payload / Code

```
robots.txt
sitemap.xml
security.txt
.git/
.env
Swagger/API Docs
Backup files
```

## Source

kjulius @ethical\_h4ck3r\_

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
