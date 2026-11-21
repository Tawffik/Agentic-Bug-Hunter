# SKILL: Authorization path parser differential — encoded semicolon, slash, and backslash

**Skill id:** `tip/authorization-path-parser-differential-encoded-semicolon-slash-and-backslash`  
**Category:** Auth Bypass, Fuzzing, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081e09e0ac4ad35dc302c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, Fuzzing, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A security layer and a resource handler may normalize or decode path components differently. Quarkus documented path-based authorization bypass conditions involving encoded semicolons (%3B) and encoded slashes (%2F) or backslashes (%5C), depending on the protected resource and affected version. The reusable primitive is to compare the path representation used by the policy engine with the final handler/resource selected.

## Payload / Code

```
Only in an authorized lab or explicitly in-scope target, start with a known protected test route and a negative control. Change one representation at a time: encoded semicolon, encoded slash, or encoded backslash. Compare policy decision, resolved route, and actual access. Do not treat a 200 response alone as proof; confirm protected content or a state change without exposing real data. Check affected versions and vendor fixes before testing.
```

## Source

Official Quarkus advisory GHSA-qcxp-gm7m-4j5v / CVE-2026-50559: [https://github.com/advisories/GHSA-qcxp-gm7m-4j5v](https://github.com/advisories/GHSA-qcxp-gm7m-4j5v)

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
