# SKILL: Advanced Dork: Private keys & certificates

**Skill id:** `tip/advanced-dork-private-keys-certificates`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808193992bcd2659e3f3fe  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب ملفات الـ private keys المكشوفة.

## Payload / Code

```
site:[target.com](http://target.com) ("BEGIN RSA PRIVATE KEY" OR "BEGIN PRIVATE KEY" OR "BEGIN OPENSSH PRIVATE KEY" OR "BEGIN CERTIFICATE")
```

## Source

[dorksearch.com](http://dorksearch.com) + OSINT guides

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
