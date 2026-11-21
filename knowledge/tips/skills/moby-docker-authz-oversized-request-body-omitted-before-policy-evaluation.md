# SKILL: Moby / Docker AuthZ — oversized request body omitted before policy evaluation

**Skill id:** `tip/moby-docker-authz-oversized-request-body-omitted-before-policy-evaluation`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081059b42e275b22cd97c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A Docker Engine authorization plugin may evaluate a request without the body when a specially crafted oversized API request triggers the condition. If the policy decision depends on body fields, the plugin may allow a request it would deny when seeing the complete body. This affects deployments using AuthZ plugins that inspect request bodies; it is not a generic Docker API bypass.

## Payload / Code

```
Research lead for an explicitly authorized Docker lab only: compare the exact same harmless API operation with a normal body and a boundary/oversized body while logging what the authorization plugin actually receives and decides. Do not test production daemons or send disruptive oversized requests without explicit permission. Confirm the plugin's input and policy decision, not just an HTTP status. Fixed in Docker Engine 29.3.1.
```

## Source

Official GitHub Advisory GHSA-x744-4wpc-v9h2 (CVE-2026-34040): [https://github.com/moby/moby/security/advisories/GHSA-x744-4wpc-v9h2](https://github.com/moby/moby/security/advisories/GHSA-x744-4wpc-v9h2)

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
