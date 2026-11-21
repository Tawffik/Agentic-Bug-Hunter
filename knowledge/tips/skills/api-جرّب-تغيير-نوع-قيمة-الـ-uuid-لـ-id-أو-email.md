# SKILL: API: جرّب تغيير نوع قيمة الـ UUID لـ ID أو Email

**Skill id:** `tip/api-جرّب-تغيير-نوع-قيمة-الـ-uuid-لـ-id-أو-email`  
**Category:** API Hacking, IDOR  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e880816397ccc4b738a4b234  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لما endpoint بيقبل UUID كـ identifier، جرّب تبعتله ID رقمي أو إيميل بدل الـ UUID. بعض الباكيندات بتعمل CASE على أكتر من نوع identifier في نفس الاستعلام، وده ممكن يفتح مسارات وصول تانية.

## Payload / Code

```
/api/user/a8ae-1322-ac09-8f90
/api/user/1
/api/user/user@a.test

SQL موازي محتمل في الباكيند:
SELECT \* FROM subscribers WHERE
  CASE
    WHEN \$1 > 0 THEN id = \$1
    WHEN \$2 != '' THEN uuid = \$2::UUID
    WHEN \$3 != '' THEN email = \$3
  END;
```

## Source

Anton @thercem an

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
