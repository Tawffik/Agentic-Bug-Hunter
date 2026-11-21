# SKILL: Advanced Dork: Swagger / OpenAPI / GraphQL docs

**Skill id:** `tip/advanced-dork-swagger-openapi-graphql-docs`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081edabb2d0ec704dda10  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب الـ API documentation المكشوفة اللي بتسهل الـ IDOR و auth bypass.

## Payload / Code

```
site:[target.com](http://target.com) (inurl:swagger OR inurl:openapi OR inurl:api-docs OR inurl:graphql) ("swagger" OR "openapi" OR "\_\_schema")
```

## Source

API fuzzing guides + real findings

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
