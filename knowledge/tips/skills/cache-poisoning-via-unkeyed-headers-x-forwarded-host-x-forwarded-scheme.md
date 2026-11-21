# SKILL: Cache Poisoning via Unkeyed Headers (X-Forwarded-Host / X-Forwarded-Scheme)

**Skill id:** `tip/cache-poisoning-via-unkeyed-headers-x-forwarded-host-x-forwarded-scheme`  
**Category:** API Hacking, XSS, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880817b8d96f63b655b2b92  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, XSS, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Inject a header the cache does not key on but the application uses for redirects, absolute URLs, or asset generation (X-Forwarded-Host, X-Forwarded-Scheme, X-Original-URL, etc.). If the response is cached with your injected value, subsequent users receive poisoned content (open redirect, XSS, or wrong origin). One request can affect many users.

## Payload / Code

```
X-Forwarded-Host: [evil.com](http://evil.com)
X-Forwarded-Scheme: http
X-Original-URL: /evil

Then force cache hit and observe Location / script src / link tags reflecting the poisoned host.
```

## Source

Twitter/X @gustavorobertux — Bug Bounty Tip #19/30 Cache poisoning (Nov 2026) + classic PortSwigger patterns

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
