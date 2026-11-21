# SKILL: CORS origin reflection + credentials = data theft

**Skill id:** `tip/cors-origin-reflection-credentials-data-theft`  
**Category:** General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880817ba83ddc9de08bb774  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو Access-Control-Allow-Origin بيعكس الـ Origin و Access-Control-Allow-Credentials: true → تقدر تسرق responses من متصفح الضحية.

## Payload / Code

```
Origin: [https://evil.com](https://evil.com)
(Check response headers for ACAO + ACAC)
```

## Source

Undercode + recent CVEs 2026

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
