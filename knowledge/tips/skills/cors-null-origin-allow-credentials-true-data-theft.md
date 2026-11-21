# SKILL: CORS null origin + Allow-Credentials: true → data theft

**Skill id:** `tip/cors-null-origin-allow-credentials-true-data-theft`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081da9c20e835bf656385  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الـ response بيرجع Access-Control-Allow-Origin: null مع Credentials true، تقدر من sandboxed iframe أو data: URI تسحب البيانات الحساسة.

## Payload / Code

```
Origin: null
# شوف لو ACAO: null و ACAC: true
```

## Source

Intigriti CORS advanced guide 2025/2026

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
