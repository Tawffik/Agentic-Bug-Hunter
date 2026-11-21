# SKILL: Client-side role / isAdmin / price tampering — verify server-side enforcement

**Skill id:** `tip/client-side-role-isadmin-price-tampering-verify-server-side-enforcement`  
**Category:** API Hacking, Auth Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e88081c1b66fe1d3ff302358  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Changing client-side values such as isAdmin, role, isAuthenticated, or price matters only if the server trusts them when authorizing an action or calculating a security-sensitive value. UI-only changes are not proof of a vulnerability.

## Payload / Code

```
With an explicitly authorized test account and test data, compare the normal request with a controlled change to a client-controlled field. Verify server-side behavior using only actions and records you own. Do not modify real purchases, payments, roles, or other users' data.
```

## Source

User-provided screenshot: response manipulation / role and price fields; normalized into a server-side authorization check

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
