# SKILL: Azure Application Gateway v2 — 403 Query String Extension Bypass (Unverified)

**Skill id:** `tip/azure-application-gateway-v2-403-query-string-extension-bypass-unverified`  
**Category:** WAF Bypass  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/403dac31e880811dbd87e6c8c15ed15e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Reported observation from an X post: a restricted URL returns HTTP 403, but adding a query parameter whose value contains the literal string .js (example: ?x=.js) reportedly changes the response and may allow access to the resource. The author suspects a Microsoft Azure Application Gateway v2 filtering/parsing behavior and says the cause is still being investigated. This is an unverified hypothesis, not a confirmed general bypass. Possible class to investigate: disagreement between gateway/WAF URL inspection and downstream application or routing interpretation of the query string.

## Payload / Code

```
Baseline: [https://authorized-target.example/restricted-path](https://authorized-target.example/restricted-path)
Comparison variant: [https://authorized-target.example/restricted-path?x=.js](https://authorized-target.example/restricted-path?x=.js)

Only replace the placeholder with a target explicitly in scope. Compare status, redirect chain, response headers, body length/hash, and whether the actual protected resource is returned. Do not treat HTTP 200 alone as proof; check for a block page, login page, or generic error.
```

## Source

[https://x.com/GodfatherOrwa/status/2114030843077259297](https://x.com/GodfatherOrwa/status/2114030843077259297)

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
