# SKILL: Swagger / OpenAPI UI → DOM XSS + Admin endpoints + leaked keys

**Skill id:** `tip/swagger-openapi-ui-dom-xss-admin-endpoints-leaked-keys`  
**Category:** XSS, Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880818b8dfad2ce7385e9f3  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ابحث عن /swagger-ui.html أو /api-docs أو /swagger.json. جرب DOM XSS في الـ UI، وكمان شوف لو فيه endpoints admin أو API keys ظاهرة في الـ response أو الـ JS. كتير من البرامج بتقبلها كـ High.

## Payload / Code

```
site:[target.com](http://target.com) inurl:swagger OR inurl:api-docs
# ثم اختبر XSS في البحث أو parameters داخل الـ UI
```

## Source

Intigriti Bug Bytes + multiple researchers (6 DOM XSS cases)

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
