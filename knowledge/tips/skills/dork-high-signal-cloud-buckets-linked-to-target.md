# SKILL: Dork (High Signal): Cloud buckets linked to target

**Skill id:** `tip/dork-high-signal-cloud-buckets-linked-to-target`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880810bbc5fd39c356407c0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب S3 / GCS / Firebase المفتوحة المرتبطة بالـ target.

## Payload / Code

```
site:[s3.amazonaws.com](http://s3.amazonaws.com) "[target.com](http://target.com)" OR site:[storage.googleapis.com](http://storage.googleapis.com) "target" OR site:[firebaseio.com](http://firebaseio.com) "target" OR site:[blob.core.windows.net](http://blob.core.windows.net) "target"
```

## Source

Common high-payout vector

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
