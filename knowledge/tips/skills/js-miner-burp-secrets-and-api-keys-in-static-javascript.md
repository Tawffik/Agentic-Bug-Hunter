# SKILL: JS Miner (Burp) — secrets and API keys in static JavaScript

**Skill id:** `tip/js-miner-burp-secrets-and-api-keys-in-static-javascript`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880818ab993da1eb227a82f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

While browsing or proxying the target, JS Miner flags high-entropy strings and known key patterns inside static JS (config.js, bundles, route maps). Treat hits as leads: public client keys ≠ server secrets; validate impact without abusing keys.

## Payload / Code

```
Burp → Extensions → JS Miner
Browse app / load JS endpoints
Review: Secrets / Credentials findings

Also manual grep in saved JS:
api\_key \| client\_secret \| Authorization \| Bearer \| AKIA \| sourceMappingURL
```

## Source

Mohamed Ahmed — JS Miner tip

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
