# SKILL: 🧩 State-Conditioned Disclosure — جرّب نفس الـObject مع اختلاف الـState

**Skill id:** `tip/state-conditioned-disclosure-جرّب-نفس-الـobject-مع-اختلاف-الـstate`  
**Category:** API Hacking, IDOR, Recon  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081f5b0fdde75a7e04cb8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, IDOR, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: أحيانًا الـauthorization/serialization يختلف حسب حالة الـobject.

States تستحق الانتباه:
draft / preview / pending / archived / shared / deleted / expired / exported.

طريقة التفكير:
object → state vocabulary من JS/API → representations المرتبطة بالـstate → compare visibility.

مثال: تقارير HackerOne المنشورة تضمنت تسريبات مرتبطة بـdrafts، pending invitations، private timelines وexports.

لا تعمل state-changing actions بشكل آلي على أهداف حقيقية. استخرج الـstate model كـhypothesis، ثم اختبر فقط ضمن scope وبأقل أثر ممكن.

## Payload / Code

```
draft
preview
pending
archived
shared
deleted
exported
```

## Source

HackerOne disclosed reports / HackerOne one-million-report dataset

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
