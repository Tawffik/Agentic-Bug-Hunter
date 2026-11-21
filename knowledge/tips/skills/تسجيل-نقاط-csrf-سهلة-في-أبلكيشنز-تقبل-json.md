# SKILL: تسجيل نقاط CSRF سهلة في أبلكيشنز تقبل JSON

**Skill id:** `tip/تسجيل-نقاط-csrf-سهلة-في-أبلكيشنز-تقبل-json`  
**Category:** CSRF  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880816e8053cd96edcd7f6d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **CSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير الأبلكيشنز الحديثة بتتأكد من CSRF token لكن مش بتتحقق كويس من Content-Type. لو لقيت طلب بيغير حالة (state-changing) مش بيتطلب token، جرّب تبعته بدون ما تشغّل CORS.

## Payload / Code

```
1) لاقي request state-changing مش محتاج token
2) اتأكد إنك تقدر تعيد إرساله بدون ما CORS تمنعك
3) اعمل HTML form بـ auto-submit وارفعه للضحية
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 29)

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
