# SKILL: Swagger / OpenAPI /api-docs exposed → full API map

**Skill id:** `tip/swagger-openapi-api-docs-exposed-full-api-map`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081929325f0e1b5a10a31  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

دور على /swagger.json, /openapi.json, /api-docs, /swagger-ui.html. لو مفتوح، عندك كل الـ endpoints والـ parameters → IDOR و auth bypass أسهل كتير.

## Payload / Code

```
[https://target.com/swagger.json](https://target.com/swagger.json)
[https://target.com/openapi.json](https://target.com/openapi.json)
[https://target.com/api-docs](https://target.com/api-docs)
```

## Source

Classic still pays + API fuzzing guides

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
