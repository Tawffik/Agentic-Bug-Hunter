# SKILL: Open Redirect — Google dorks and common parameter names

**Skill id:** `tip/open-redirect-google-dorks-and-common-parameter-names`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808148a6b0c3c15f362aef  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Search engines index login and redirect endpoints. Dorks with inurl:return\_to (and similar) surface candidates; then test parameter values for open redirect. Long list of parameter names increases coverage on login/logout flows.

## Payload / Code

```
site:.[target.com](http://target.com) inurl:return\_to
site:.[target.com](http://target.com) inurl:redirect
site:.[target.com](http://target.com) inurl:url=
site:.[target.com](http://target.com) inurl:next=

Params: return, return\_to, return\_url, redirect, redirect\_to, redirect\_uri, url, next, goto, destination, continue, callback, rurl, dest, forward, return\_path

Test: //evil.example
```

## Source

Anton — Google Dork for Open Redirect or XSS URLs · Sep 2023

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
