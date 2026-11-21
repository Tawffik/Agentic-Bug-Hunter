# SKILL: JSON: مفاتيح مكررة ممكن تفصل الـ Auth عن التنفيذ

**Skill id:** `tip/json-مفاتيح-مكررة-ممكن-تفصل-الـ-auth-عن-التنفيذ`  
**Category:** API Hacking, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081eda815e7680f716660  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الـ middlewares بتقرأ أول مفتاح مكرر في الـ JSON للـ authentication، لكن الـ backend بيعالج آخر قيمة. الفجوة دي ممكن تخليك تعدي auth على حساب وتنفّذ عملية على حساب تاني.

## Payload / Code

```
❌ \{"Account": 2222\}
✅ \{"Account": 2222, "Account": 3333, "Account": 5555\}
```

## Source

vulnX @vuln\_X

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
