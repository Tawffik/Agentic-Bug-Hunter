# SKILL: Advanced Dork: Firebase / S3 public buckets

**Skill id:** `tip/advanced-dork-firebase-s3-public-buckets`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081c3833ee1400a28e9d4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب buckets و Firebase المفتوحة المرتبطة بالـ target.

## Payload / Code

```
site:[s3.amazonaws.com](http://s3.amazonaws.com) "[target.com](http://target.com)" OR site:[firebaseio.com](http://firebaseio.com) "target" OR site:[storage.googleapis.com](http://storage.googleapis.com) "target"
```

## Source

OSINT 2026 guides

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
