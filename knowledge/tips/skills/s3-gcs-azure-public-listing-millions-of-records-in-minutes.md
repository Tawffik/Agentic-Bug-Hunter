# SKILL: S3 / GCS / Azure public listing → millions of records in minutes

**Skill id:** `tip/s3-gcs-azure-public-listing-millions-of-records-in-minutes`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081f5b828c0bca03ba34f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعد ما تلاقي الـ bucket، جرب list بدون credentials. لو نجح، حمل الملفات الحساسة (PII، backups، configs). كتير من البرامج بتدفع High/Critical على ده.

## Payload / Code

```
aws s3 ls s3://bucket --no-sign-request
gsutil ls gs://bucket
az storage blob list --container-name ... --auth-mode login
```

## Source

Multiple 2025-2026 cases (one \$10k in 15 min)

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
