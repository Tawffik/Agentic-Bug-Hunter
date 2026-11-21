# SKILL: Path policy vs execution parser: compare both views

**Skill id:** `tip/path-policy-vs-execution-parser-compare-both-views`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e8808166a67ef338dc48a1c5  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

When a gateway/security layer and the final router decode or normalize a path differently, the first layer may authorize one representation while the second executes another. Compare the two views and prove the final resource reached.

## Payload / Code

```
Use only inside a lab or explicitly authorized target. Mutate one representation at a time: encoded semicolon, encoded slash/backslash, and double-encoding; verify the final route/resource, not just the status code.
```

## Source

[https://github.com/quarkusio/quarkus/security/advisories/GHSA-qcxp-gm7m-4j5v](https://github.com/quarkusio/quarkus/security/advisories/GHSA-qcxp-gm7m-4j5v)

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
