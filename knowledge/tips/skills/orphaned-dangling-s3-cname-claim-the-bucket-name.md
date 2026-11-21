# SKILL: Orphaned / dangling S3 CNAME → claim the bucket name

**Skill id:** `tip/orphaned-dangling-s3-cname-claim-the-bucket-name`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081f28607ed7ec320ae11  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو subdomain CNAME بيشير لـ [s3.amazonaws.com](http://s3.amazonaws.com) والـ bucket اتمسح أو مش موجود، تقدر تعمل bucket بنفس الاسم وتستقبل الطلبات (subdomain takeover variant).

## Payload / Code

```
dig CNAME [assets.target.com](http://assets.target.com)
# لو يشير لـ [nonexistent-bucket.s3.amazonaws.com](http://nonexistent-bucket.s3.amazonaws.com) → claim it
```

## Source

Cloud bucket hacking guides 2026

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
