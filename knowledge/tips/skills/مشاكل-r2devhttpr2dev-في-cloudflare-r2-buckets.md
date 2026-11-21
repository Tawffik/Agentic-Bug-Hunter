# SKILL: مشاكل [R2.dev](http://R2.dev) في Cloudflare R2 Buckets

**Skill id:** `tip/مشاكل-r2devhttpr2dev-في-cloudflare-r2-buckets`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880817897c2f7b77d3e6504  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Cloudflare R2 فيه فيچر اسمه [R2.dev](http://R2.dev) بيسمح بالوصول العام لمحتوى الـ bucket لأغراض الاختبار. لو اتساب مفعّل في Production، ممكن يطلع ملفات حساسة وbackups وبيانات.

## Payload / Code

```
دور على URLs من نوع: pub-\.[r2.dev](http://r2.dev)
وجرّب تشوف هل الـ bucket مفتوح للقراءة العامة بدون تأمين
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 13)

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
