# SKILL: security.txt + .well-known/ → contact + policy info

**Skill id:** `tip/securitytxt-well-known-contact-policy-info`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081dd9595f4bdff390801  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مش بس info، أحيانًا بتكشف internal contacts أو bug bounty policy أو حتى keys. جرب /.well-known/security.txt و /.well-known/

## Payload / Code

```
[https://target.com/.well-known/security.txt](https://target.com/.well-known/security.txt)
[https://target.com/.well-known/](https://target.com/.well-known/)
```

## Source

Intigriti BugQuest Day 9

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
