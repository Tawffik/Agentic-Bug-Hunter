# SKILL: 🔔 Bug Bounty Tip — Parameter Swap → Unauthorized Workspace Access

**Skill id:** `tip/bug-bounty-tip-parameter-swap-unauthorized-workspace-access`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e5dac31e8808189a39ece320e3e27aa  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Type: Bug Pattern
Use when: the application has workspaces, organizations, projects, teams, or shared resources.

Where to look → GET/POST/PATCH requests containing workspace\_id, org\_id, project\_id, member\_id, or similar object identifiers.

What to test → Repeat the same request with a second authorized test account and swap only the object identifier. Also test whether the API trusts a client-controlled workspace or organization field.

Primitive / bypass → Broken object-level authorization (BOLA/IDOR): the server checks that the user is logged in, but not that the object belongs to the user’s tenant.

Validation / impact → Confirm access to a resource owned by the other test account without changing unrelated fields. Capture the minimum proof: request, changed identifier, response difference, and the cross-tenant data or action exposed. Stop at one harmless object and remain inside program scope.

## Payload / Code

```
Change only the object identifier in an authorized two-account test. Do not enumerate IDs or access unrelated users.
```

## Source

[https://www.bugbountydirectory.com/blogs/how-a-little-modification-of-a-request-parameter-led-to-unauthorized-access-to-private-workspaces](https://www.bugbountydirectory.com/blogs/how-a-little-modification-of-a-request-parameter-led-to-unauthorized-access-to-private-workspaces)

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
