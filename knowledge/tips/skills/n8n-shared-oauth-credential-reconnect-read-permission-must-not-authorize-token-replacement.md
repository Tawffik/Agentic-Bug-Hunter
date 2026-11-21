# SKILL: n8n shared OAuth credential reconnect — read permission must not authorize token replacement

**Skill id:** `tip/n8n-shared-oauth-credential-reconnect-read-permission-must-not-authorize-token-replacement`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e880817aa890cfc525ca1969  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Affected OAuth reconnect endpoints authorized the operation with credential:read rather than credential:update. A read-only user of a shared credential could initiate reconnect and replace its stored token material with a token for an external account they controlled, changing the identity used by workflows. The core primitive is an authorization-level mismatch between viewing a credential and mutating its linked identity.

## Payload / Code

```
In an authorized lab with a shared dummy OAuth credential, compare a read-only member's ability to view the credential versus reconnect/update it. Confirm whether the stored provider identity changes and whether workflows use the new identity; do not touch real shared credentials or send data to external accounts. The advisory lists fixes in 1.123.43, 2.20.7, and 2.21.1.
```

## Source

Official n8n GitHub Advisory GHSA-6h4j-wcr9-2vg7 (published 2026-05-13): [https://github.com/n8n-io/n8n/security/advisories/GHSA-6h4j-wcr9-2vg7](https://github.com/n8n-io/n8n/security/advisories/GHSA-6h4j-wcr9-2vg7)

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
