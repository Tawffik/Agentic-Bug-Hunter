# SKILL: 404 Subdomains — Backend errors, S3 paths, and leaked stack info

**Skill id:** `tip/404-subdomains-backend-errors-s3-paths-and-leaked-stack-info`  
**Category:** Recon, Subdomain Enum  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081fb807ac1f69349caa1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Subdomains that return 404 are often ignored. Hitting a non-existent path on those hosts can still surface backend error pages, stack traces, internal paths, S3 references, or dev leftovers that never appear on the main site.

## Payload / Code

```
1) Enumerate subs → httpx
2) Keep hosts with interesting 404/500 behavior
3) Probe: /random404, /nonexistent, /.env, /debug
4) Review body for stack traces, bucket URLs, internal hostnames

Example idea:
[https://test.api.target.com/random404](https://test.api.target.com/random404)
```

## Source

Hatem Aliyan — Bug Bounty Tip (404 pages)

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
