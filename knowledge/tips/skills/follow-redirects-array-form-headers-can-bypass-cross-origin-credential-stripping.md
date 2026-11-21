# SKILL: follow-redirects — array-form headers can bypass cross-origin credential stripping

**Skill id:** `tip/follow-redirects-array-form-headers-can-bypass-cross-origin-credential-stripping`  
**Category:** Auth Bypass, API Hacking, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e880814ca8d9da2ecedced33  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

In follow-redirects 1.16.0, sensitive-header removal iterated headers as though they were a plain object. Node also accepts an array of alternating header names and values; in that form, iteration sees numeric indices, so cross-host stripping can silently fail and forward Authorization/Cookie/Proxy-Authorization or configured sensitive headers. Fixed in 1.16.1.

## Payload / Code

```
In a local test with two HTTP(S) origins you control, send a harmless canary credential header through a redirect from origin A to origin B. Compare object-form and array-form headers and inspect what B receives. Never use real credentials or a third-party redirect target. Check the installed dependency version and confirm the redirect crosses hosts or downgrades protocol.
```

## Source

Official GitHub Advisory GHSA-q3jh-wrc6-jgq8 (published 2026-10-01): [https://github.com/follow-redirects/follow-redirects/security/advisories/GHSA-q3jh-wrc6-jgq8](https://github.com/follow-redirects/follow-redirects/security/advisories/GHSA-q3jh-wrc6-jgq8)

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
