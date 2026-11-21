# SKILL: NoSQL Injection عبر Parameter Arrays لتجاوز قيود الـ Content-Type

**Skill id:** `tip/nosql-injection-عبر-parameter-arrays-لتجاوز-قيود-الـ-content-type`  
**Category:** SQLi  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081e39d1de6ca4e03dcd7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الأبلكيشن بيرفض يقبل JSON للـ NoSQLi العادي، لكن بيقبل form data (application/x-www-form-urlencoded)، جرّب array notation في الـ param — بعض المكتبات بتحول array notation في form data لأوبجيكت في الباكيند، وده بيخليك تحقن عمليات NoSQL زي \$ne حتى مع content-type مقيّد.

## Payload / Code

```
بدل [email=victim@mail.com](mailto:email=victim@mail.com)&password=x
جرّب: password\[\$ne\]=null
أو: token\[\$ne\]=null
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 27)

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
