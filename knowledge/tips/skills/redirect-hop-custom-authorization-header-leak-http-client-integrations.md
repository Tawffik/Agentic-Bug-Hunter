# SKILL: Redirect Hop → Custom Authorization Header Leak (HTTP Client Integrations)

**Skill id:** `tip/redirect-hop-custom-authorization-header-leak-http-client-integrations`  
**Category:** SSRF, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808103b311d8d813d1a681  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A server-side feature fetches a URL using a client configured with an API key or custom Authorization header. If the first endpoint returns a redirect to a different host and the HTTP client forwards sensitive headers across that redirect, the destination may receive credentials. This is a separate failure mode from browser Referer leakage: the secret travels in the outbound request headers. Recent research published 18 Oct 2026 compared multiple HTTP clients and found that behavior differs by library and version. Hunt only in-scope URL-fetching/integration features; validate with a researcher-controlled endpoint or approved callback, never a third-party host.

## Payload / Code

```
Test plan (authorized target only):
1. Find a feature that fetches a URL server-side (webhook tester, image importer, URL preview, notification integration, PDF/URL fetcher).
2. Use a controlled endpoint A that responds with HTTP 302 to a controlled endpoint B.
3. If the feature legitimately attaches credentials to outbound requests, inspect whether B receives Authorization, Cookie, or custom API-key headers.
4. Compare direct-fetch behavior against the redirect chain; vary same-origin vs cross-origin redirect and HTTP client/library where evidence is available.
5. Report only if a sensitive header crosses an origin boundary and creates real unauthorized access; redact tokens in evidence.
```

## Source

[https://safeguard.sh/resources/blog/http-client-redirect-header-leak-authorization-api-key-2026](https://safeguard.sh/resources/blog/http-client-redirect-header-leak-authorization-api-key-2026)

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
