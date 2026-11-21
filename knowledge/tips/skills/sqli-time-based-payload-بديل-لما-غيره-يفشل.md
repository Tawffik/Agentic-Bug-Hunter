# SKILL: SQLi: Time-based payload بديل لما غيره يفشل

**Skill id:** `tip/sqli-time-based-payload-بديل-لما-غيره-يفشل`  
**Category:** SQLi  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081b18386ca737db10b6d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Payload مبني على PostgreSQL time-based blind SQLi، بيستخدم pg\_sleep لقياس التأخير في الرد والتأكد من وجود الثغرة. مفيد يتضاف لِـ wordlist بتاع SQLi.

## Payload / Code

```
''\|\|(select 1 from (select pg\_sleep(6))x)\|\|'
```

## Source

Brut 🇮🇳 @wtf\_yodhha — Credit: @GodfatherOrwa

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
