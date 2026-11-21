# SKILL: SQLi: كشف الحقن في باراميترات رقمية عبر إضافة تعبير حسابي

**Skill id:** `tip/sqli-كشف-الحقن-في-باراميترات-رقمية-عبر-إضافة-تعبير-حسابي`  
**Category:** SQLi  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e880817689b9c7a46647ca41  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الباراميتر بيتحط جوه استعلام SQL بدون تنقية، تعبير حسابي زي 31338-1 هيتحسب في الاستعلام ويرجع نفس نتيجة 31337. ده دليل قوي على وجود SQL Injection في الباراميترات الرقمية.

## Payload / Code

```
Query: ?id=31337 → النتيجة: عنصر بـ ID 31337
Query: ?id=31338-1 → النتيجة: نفس العنصر بـ ID 31337 (لأن 31338-1=31337)
```

## Source

Anton @thercem an — 30 Sep 23

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
