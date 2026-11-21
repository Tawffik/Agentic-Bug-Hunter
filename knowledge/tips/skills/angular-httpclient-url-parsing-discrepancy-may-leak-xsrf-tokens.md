# SKILL: Angular HttpClient — URL parsing discrepancy may leak XSRF tokens

**Skill id:** `tip/angular-httpclient-url-parsing-discrepancy-may-leak-xsrf-tokens`  
**Category:** CSRF, Fuzzing, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081f6a157f78582dee1d3  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **CSRF, Fuzzing, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Angular's HTTP client had an XSRF token leakage issue related to a URL-parsing discrepancy, described as an incomplete fix for CVE-2025-66035. The useful testing pattern is to compare how the framework classifies a request URL against how the browser/network layer resolves the final destination; token attachment must follow the intended same-origin policy.

## Payload / Code

```
In a local app using an affected Angular version, test only controlled same-origin and cross-origin URLs and observe whether the XSRF header is attached to a request that resolves cross-origin. Use a dummy token and a local receiver; do not collect real anti-CSRF tokens from production users. Read the advisory for affected/fixed versions and upgrade guidance.
```

## Source

Official Angular Advisory GHSA-jfgx-762w-99vr (2026-10-16): [https://github.com/angular/angular/security/advisories/GHSA-jfgx-762w-99vr](https://github.com/angular/angular/security/advisories/GHSA-jfgx-762w-99vr)

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
