# SKILL: Hasura GraphQL engine → missing authorization on mutations

**Skill id:** `tip/hasura-graphql-engine-missing-authorization-on-mutations`  
**Category:** API Hacking, Auth Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081399c08c49952e2605e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Hasura قد ينشئ عمليات GraphQL تلقائيًا، لكن الأثر يعتمد على صلاحيات الدور والـ row/column permissions. لا تستخدم mutation لتغيير دور إلى admin أو حذف/تعديل بيانات حقيقية. اختبر فقط سجلًا تجريبيًا تملكه وبما تسمح به قواعد البرنامج، وقارن صلاحيات الأدوار لإثبات الخلل.

## Payload / Code

```
mutation \{ update\_table\_by\_pk(pk\_columns: \{id: "..."\}, \_set: \{role: "admin"\}) \{ id \} \}
```

## Source

Mohamed Atef writeup 2026 (High)

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
