# SKILL: ⏳ Historical API Drift — Wayback لاستخراج APIs القديمة ثم اختبار وجودها حاليًا

**Skill id:** `tip/historical-api-drift-wayback-لاستخراج-apis-القديمة-ثم-اختبار-وجودها-حاليًا`  
**Category:** Recon, API Hacking, Subdomain Enum  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081ef9b3cf303eb6b32fe  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking, Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: استخدم الـhistorical JS/pages لاكتشاف functionality قديمة، ثم قارنها بالـcurrent attack surface.

workflow:
old JS/page → extract routes/methods/parameters → normalize → current validation → classify:
- removed
- still alive
- redirected
- changed behavior
- replaced by newer API

القيمة: بدل قائمة Wayback ضخمة، تحصل على historical → current differential.

لا تفترض أن legacy endpoint vulnerability؛ قيم authorization/data exposure بعد إثبات أنه ما زال reachable.

## Payload / Code

```
old.js
  ↓
/api/v1/legacy
  ↓
current host
  ↓
read-only validation
```

## Source

Wayback-based bug bounty research + disclosed historical-functionality cases

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
