# SKILL: 🔎 Representation Differential — نفس الـObject بصيغ مختلفة ممكن يكشف Fields زيادة

**Skill id:** `tip/representation-differential-نفس-الـobject-بصيغ-مختلفة-ممكن-يكشف-fields-زيادة`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081fca9f4cbfb381a56ac  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: لو نفس الـresource له أكثر من representation، لا تفترض أن كل serializer يعيد نفس الحقول.

ابحث عن:
- /resource → /resource.json
- ?format=json
- Accept: application/json
- XML/API representations عندما تكون موجودة

ما الذي تقارنه؟
Status + Content-Type + JSON keys + nested objects + metadata + authorization-sensitive fields.

الـpivot: HTML/public representation → alternate representation → schema diff → sensitive-field candidate.

مثال bounty حقيقي: HackerOne وثّقت حالة /reports/:id.json كشفت بيانات حساسة لم تكن ظاهرة في representation العادية، مع bounty كبير جدًا.

مهم: وجود .json أو اختلاف schema وحده ليس ثغرة؛ المطلوب field/relationship حساس خارج الـintended visibility.

## Payload / Code

```
/page
/page.json
/page?format=json

Accept: application/json
```

## Source

HackerOne Hacktivity — disclosed report involving /reports/:id.json; pattern validated in bounty research

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
