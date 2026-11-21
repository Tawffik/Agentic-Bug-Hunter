# SKILL: Treat negative parser cases as evidence

**Skill id:** `tip/treat-negative-parser-cases-as-evidence`  
**Category:** Auth Bypass, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e88081e39f26c84aaf7d2503  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A strong differential test records which variants do not work and why. This prevents turning every encoding mutation into a false positive and helps identify the exact boundary where parser views diverge.

## Payload / Code

```
For each variant, record: security-layer interpretation, routing-layer interpretation, final resource, and observed side effect. Include confirmed non-exploitable cases.
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
