# SKILL: فزّينج بأكتر من HTTP Method مش بس GET

**Skill id:** `tip/فزّينج-بأكتر-من-http-method-مش-بس-get`  
**Category:** Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081f5b5f3f64ed99d01b3  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير من الـ endpoints وAPI routes معمولة ترد فقط على methods معينة (POST/PUT/DELETE) ومش بتظهر في فزّينج GET العادي. فزّينج بأكتر من method بيكشف paths مخفية ما كانت هتطلع مع GET لوحده.

## Payload / Code

```
ffuf -u [https://target.com/api/FUZZ](https://target.com/api/FUZZ) -w wordlist.txt -X POST
ffuf -u [https://target.com/api/FUZZ](https://target.com/api/FUZZ) -w wordlist.txt -X PUT
ffuf -u [https://target.com/api/FUZZ](https://target.com/api/FUZZ) -w wordlist.txt -X DELETE
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 7)

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
