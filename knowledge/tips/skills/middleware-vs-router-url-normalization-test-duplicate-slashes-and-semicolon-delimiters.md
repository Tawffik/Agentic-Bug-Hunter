# SKILL: Middleware vs Router URL Normalization — test duplicate slashes and semicolon delimiters

**Skill id:** `tip/middleware-vs-router-url-normalization-test-duplicate-slashes-and-semicolon-delimiters`  
**Category:** Auth Bypass, Fuzzing, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081f49ebce67779c0c746  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, Fuzzing, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

When a router normalizes a path but path-scoped authentication middleware receives the original representation, the two layers can disagree about which route is being requested. In affected @fastify/express versions, duplicate slashes or semicolon delimiters could cause middleware to be skipped when the corresponding Fastify normalization options were enabled. This depends on the stack and configuration; do not assume every app is vulnerable.

## Payload / Code

```
In a permitted test environment, identify the framework, adapter, versions, and active normalization options. Compare a benign protected route using its canonical path with controlled variants containing duplicate slashes or a semicolon delimiter. Record the router's resolved route and whether the auth middleware ran. Confirm actual protected-resource access, not just a different status code. Advisory: affected \<=4.0.4; fixed in 4.0.5.
```

## Source

Official GitHub Advisory GHSA-6hw5-45gm-fj88 / CVE-2026-33808: [https://github.com/fastify/fastify-express/security/advisories/GHSA-6hw5-45gm-fj88](https://github.com/fastify/fastify-express/security/advisories/GHSA-6hw5-45gm-fj88)

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
