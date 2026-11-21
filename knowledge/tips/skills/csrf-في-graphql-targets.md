# SKILL: CSRF في GraphQL Targets

**Skill id:** `tip/csrf-في-graphql-targets`  
**Category:** CSRF  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808140bb98dd936ff9f4da  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **CSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

GraphQL مالوش فيها حماية مدمجة ضد CSRF. لو لقيت طلب بيغير حالة بدون token، والـ backend بيقبل content-type غير JSON، تقدر تعمل CSRF form عادي ليه.

## Payload / Code

```
1) لاقي mutation بيغير حالة مش محتاج token
2) غيّر content-type من application/json إلى application/x-www-form-urlencoded
3) اعمل form html بتبعت الـ mutation body مباشرة
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 30)

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
