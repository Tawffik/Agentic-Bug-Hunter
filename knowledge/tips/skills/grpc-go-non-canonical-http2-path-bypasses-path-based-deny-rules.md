# SKILL: gRPC-Go — non-canonical HTTP/2 :path bypasses path-based deny rules

**Skill id:** `tip/grpc-go-non-canonical-http2-path-bypasses-path-based-deny-rules`  
**Category:** Auth Bypass, API Hacking, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081618158d969dc3f7761  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Affected gRPC-Go versions accepted an HTTP/2 :path without the required leading slash for routing, while path-based authorization interceptors evaluated the non-canonical path. Deny rules for canonical paths could therefore fail when a fallback allow rule existed. The affected setup requires path-based authorization and this policy shape; this is not a universal gRPC bypass.

## Payload / Code

```
In an authorized test server using an affected version, compare canonical and non-canonical :path representations for a harmless test method. Inspect the router's selected handler and the authorization interceptor's observed method/path. Verify whether the deny rule actually blocks the request; never send malformed raw HTTP/2 frames to third-party systems. Fixed in gRPC-Go 1.79.3.
```

## Source

Official GitHub Advisory GHSA-p77j-4mvh-x3m3 (CVE-2026-33186): [https://github.com/grpc/grpc-go/security/advisories/GHSA-p77j-4mvh-x3m3](https://github.com/grpc/grpc-go/security/advisories/GHSA-p77j-4mvh-x3m3)

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
