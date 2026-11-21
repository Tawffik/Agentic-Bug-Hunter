# SKILL: 🔍 Public JSON/Search Response — الـSearch endpoint قد يعرض Metadata أكثر من الصفحة

**Skill id:** `tip/public-jsonsearch-response-الـsearch-endpoint-قد-يعرض-metadata-أكثر-من-الصفحة`  
**Category:** Recon, API Hacking, IDOR  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e880814ca492d70260b9a373  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking, IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: لا تركز على HTML search فقط. بعض التطبيقات تملك JSON/search representations تعيد metadata إضافية.

فتّش عن:
/search.json, /users.json, /reports.json, /index.json, ?query=, ?format=json.

قارن: HTML result vs JSON result vs authenticated/unauthenticated visibility.

أمثلة منشورة: datasets لتقارير HackerOne تحتوي حالات search JSON responses كشفت private-program metadata وبيانات لم تكن ظاهرة في الواجهة.

مهم: لا تعتمد على أسماء endpoints فقط؛ استخرجها من JS/API/network traffic.

## Payload / Code

```
/search.json
/users.json
/reports.json
/index.json
?format=json
```

## Source

HackerOne one-million-report dataset / disclosed search-response disclosure cases

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
