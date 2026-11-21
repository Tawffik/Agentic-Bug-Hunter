# SKILL: API Debug /env /status endpoints → \$3,000 Bounty (Secret Hunter case)

**Skill id:** `tip/api-debug-env-status-endpoints-3000-bounty-secret-hunter-case`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081fcad01fe34ec88f8e0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كثير APIs بتسيب /debug أو /env أو /\_debug أو /health مع verbose mode. بيرجع environment variables كاملة. استخدم ffuf بقائمة debug endpoints.

## Payload / Code

```
ffuf -u [https://target.com/api/FUZZ](https://target.com/api/FUZZ) -w debug\_endpoints.txt -mc 200
# قائمة: debug, env, status, health, \_debug, actuator/env
```

## Source

Undercode Testing writeup – \$3,000 paid

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
