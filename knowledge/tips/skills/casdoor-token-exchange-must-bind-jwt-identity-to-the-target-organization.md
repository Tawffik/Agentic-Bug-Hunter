# SKILL: Casdoor — token exchange must bind JWT identity to the target organization

**Skill id:** `tip/casdoor-token-exchange-must-bind-jwt-identity-to-the-target-organization`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081d2842ae3e6ead7ab47  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

The reported Casdoor issue involved token exchange validating a JWT signature without verifying that the token's user belonged to the same organization as the target application. A valid token from one organization could cross an organization boundary if the missing binding check and affected versions were present.

## Payload / Code

```
For an authorized lab with two test organizations and accounts, test whether token exchange enforces both signature validity and organization/tenant membership. Use only test identities and non-sensitive scopes; record the subject, issuer, organization, target app, and resulting permissions. Do not replay real users' tokens. Advisory says affected versions were fixed in 2.387.0.
```

## Source

GitHub Advisory GHSA-c9w5-qp6m-m395 (CVE-2026-9094): [https://github.com/advisories/GHSA-c9w5-qp6m-m395](https://github.com/advisories/GHSA-c9w5-qp6m-m395)

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
