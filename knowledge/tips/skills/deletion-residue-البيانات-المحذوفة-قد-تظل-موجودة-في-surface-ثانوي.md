# SKILL: 🗑️ Deletion Residue — البيانات المحذوفة قد تظل موجودة في Surface ثانوي

**Skill id:** `tip/deletion-residue-البيانات-المحذوفة-قد-تظل-موجودة-في-surface-ثانوي`  
**Category:** Recon, API Hacking, IDOR  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e880812c8ceffb618ac621dc  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking, IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: deletion من الـprimary surface لا يعني بالضرورة حذف كل copies/references.

فتّش عن:
deleted object → draft/preview → export → attachment → CDN/object URL → email/notification copy → API reference.

الـpivot: object ID أو attachment ID المعروف → ابحث عن representations أخرى لنفس identifier.

مثال حقيقي: HackerOne disclosed reports تضمنت حالات أمكن فيها الحصول على copies من deleted attachments عبر secondary functionality.

قاعدة: لا تعتبر archive/backup مجرد finding؛ يجب إثبات أن artifact ما زال يتيح بيانات يفترض أنها لم تعد متاحة.

## Payload / Code

```
object\_id
attachment\_id
download\_id
export\_id
```

## Source

HackerOne disclosed reports — deleted attachment / secondary-copy disclosure cases

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
