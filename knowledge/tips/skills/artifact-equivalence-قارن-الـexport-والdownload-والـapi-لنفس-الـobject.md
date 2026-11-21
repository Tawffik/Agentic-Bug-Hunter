# SKILL: 📦 Artifact Equivalence — قارن الـExport والDownload والـAPI لنفس الـObject

**Skill id:** `tip/artifact-equivalence-قارن-الـexport-والdownload-والـapi-لنفس-الـobject`  
**Category:** API Hacking, IDOR, Recon  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081d9b0b8d207cd9f01c6  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, IDOR, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: نفس البيانات قد تكون متاحة عبر أكثر من artifact: page, JSON, export, download, PDF, ZIP, attachment.

الـworkflow:
1. حدد object identifier.
2. اجمع representations المرتبطة به.
3. قارن ownership/authorization/fields/attachments/metadata.
4. ابحث عن artifact يكشف أكثر من المصدر الأساسي.

أمثلة حقيقية: HackerOne disclosures تضمنت partial disclosure عبر Export as .zip وتسريبات مرتبطة بالـexports/attachments.

Signal قوي: نفس object + نفس user context + artifact آخر يعيد بيانات لا تعيدها الواجهة/endpoint الأساسي.

## Payload / Code

```
/report/123
/report/123.json
/report/123/export
/report/123/download
/report/123.pdf
/report/[123.zip](http://123.zip)
```

## Source

HackerOne Hacktivity / disclosed bounty reports — Export and attachment disclosure cases

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
