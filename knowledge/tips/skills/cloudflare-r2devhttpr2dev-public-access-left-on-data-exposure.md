# SKILL: Cloudflare [R2.dev](http://R2.dev) public access left on → data exposure

**Skill id:** `tip/cloudflare-r2devhttpr2dev-public-access-left-on-data-exposure`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808139994de6087afa05be  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Cloudflare R2 buckets ممكن تتفتح عبر [R2.dev](http://R2.dev) للتجربة. لو المطور نسي يقفلها، تقدر توصل للـ objects بدون auth. دور على \*.[r2.dev](http://r2.dev) أو CNAME لـ R2.

## Payload / Code

```
[https://bucket-name.account-id.r2.dev/](https://bucket-name.account-id.r2.dev/)
# أو ابحث عن [r2.dev](http://r2.dev) في JS / DNS
```

## Source

Intigriti complete guide (updated 2026)

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
