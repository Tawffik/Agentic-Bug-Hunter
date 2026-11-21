# SKILL: follow-redirects — regex metacharacters in sensitiveHeaders may evade stripping

**Skill id:** `tip/follow-redirects-regex-metacharacters-in-sensitiveheaders-may-evade-stripping`  
**Category:** Auth Bypass, API Hacking, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081128961df3eb085171c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

The sensitiveHeaders option introduced in follow-redirects 1.16.0 builds a regular expression from configured header names, but the escaping routine omitted some metacharacters. Valid header names containing characters such as \^ or \| could therefore fail to match the intended name and not be stripped on a cross-origin redirect. Fixed in 1.16.1.

## Payload / Code

```
In a local two-origin test, configure a harmless canary header name containing a supported token metacharacter and mark it sensitive. Trigger a cross-origin redirect and verify whether the header is removed. Use only test values; do not attempt to extract credentials from live services. Distinguish this option-specific issue from the separate array-form header handling issue.
```

## Source

Official GitHub Advisory GHSA-8r9p-f939-6h3c (published 2026-10-01): [https://github.com/follow-redirects/follow-redirects/security/advisories/GHSA-8r9p-f939-6h3c](https://github.com/follow-redirects/follow-redirects/security/advisories/GHSA-8r9p-f939-6h3c)

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
