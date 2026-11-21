# SKILL: n8n OAuth callback — bind the completing browser session to the flow initiator

**Skill id:** `tip/n8n-oauth-callback-bind-the-completing-browser-session-to-the-flow-initiator`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081f9b72ad3d3646e1bc9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

The reported Enterprise issue allowed an OAuth2 credential callback to complete without requiring the browser to be authenticated as the user who initiated the dynamic-credential connect flow. If another person completed the provider consent, their tokens could be stored under the initiating member's identity. This is distinct from checking OAuth state alone: the callback must also preserve the intended user/browser binding.

## Payload / Code

```
In a lab or explicitly authorized n8n Enterprise test with two controlled accounts and a test OAuth provider, start a dynamic-credential connect flow as Account A, then verify that completion is rejected when performed in an unrelated browser/session for Account B. Use a dummy provider and revoke test tokens afterward. Do not trick real users into authorizing a flow. The advisory lists fixes in 2.46.1, 2.45.5, and 3.0.1.
```

## Source

Official n8n GitHub Advisory GHSA-426f-xmcv-g8pg (published 2026-10-28): [https://github.com/n8n-io/n8n/security/advisories/GHSA-426f-xmcv-g8pg](https://github.com/n8n-io/n8n/security/advisories/GHSA-426f-xmcv-g8pg)

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
