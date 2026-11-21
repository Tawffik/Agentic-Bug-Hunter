# SKILL: SSRF via webhook / import / URL fetch features

**Skill id:** `tip/ssrf-via-webhook-import-url-fetch-features`  
**Category:** SSRF  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e8808191902be6aa3f240e81  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أي feature بتجيب URL من السيرفر (webhook, avatar import, PDF from URL) → جرب [http://169.254.169.254](http://169.254.169.254) أو internal.

## Payload / Code

```
url=[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)
```

## Source

Top paying classes 2026

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
