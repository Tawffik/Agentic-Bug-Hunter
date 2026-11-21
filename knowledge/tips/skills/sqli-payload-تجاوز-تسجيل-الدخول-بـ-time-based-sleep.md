# SKILL: SQLi: Payload تجاوز تسجيل الدخول بـ time-based sleep

**Skill id:** `tip/sqli-payload-تجاوز-تسجيل-الدخول-بـ-time-based-sleep`  
**Category:** SQLi, Auth Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e8808115abe3ccb0c21d70af  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

حقن payload في حقل زي username لقياس تأخير الاستجابة (5 ثواني) والتأكد من وجود SQL Injection قبل ما تبني عليه استغلال أعمق زي تجاوز الـ authentication.

## Payload / Code

```
'%2b(select\*from(select(sleep(5)))a)%2b'
```

## Source

SusluSec @suslu7616 — #sqli

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
