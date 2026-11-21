# SKILL: Dork (High Signal): API Docs & Swagger / GraphQL / Redoc

**Skill id:** `tip/dork-high-signal-api-docs-swagger-graphql-redoc`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081fabaa5fd247f279568  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب الـ API documentation اللي بتسهل IDOR و auth issues.

## Payload / Code

```
site:[target.com](http://target.com) (inurl:apidocs OR inurl:api-docs OR inurl:swagger OR inurl:api-explorer OR inurl:redoc OR inurl:openapi OR inurl:graphql OR intitle:"Swagger UI")
```

## Source

Multiple bounty writeups + Intigriti guides

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
