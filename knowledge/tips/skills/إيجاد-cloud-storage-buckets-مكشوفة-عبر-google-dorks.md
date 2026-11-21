# SKILL: إيجاد Cloud Storage Buckets مكشوفة عبر Google Dorks

**Skill id:** `tip/إيجاد-cloud-storage-buckets-مكشوفة-عبر-google-dorks`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880812c92abda6988d617d7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الشركات بتستخدم Cloud Storage Buckets (S3, Azure Blob, GCS) وبتسميها بأسماء متوقعة، ودي بتطلعها قابلة للاكتشاف عبر Google dorks بسيطة.

## Payload / Code

```
site:[s3.amazonaws.com](http://s3.amazonaws.com) "target"
site:[blob.core.windows.net](http://blob.core.windows.net) "target"
site:[storage.googleapis.com](http://storage.googleapis.com) "target"
intext:"target" site:[s3.amazonaws.com](http://s3.amazonaws.com)
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 12)

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
