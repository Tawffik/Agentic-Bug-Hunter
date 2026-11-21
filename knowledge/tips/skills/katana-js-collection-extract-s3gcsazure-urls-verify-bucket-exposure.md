# SKILL: Katana JS collection → extract S3/GCS/Azure URLs → verify bucket exposure

**Skill id:** `tip/katana-js-collection-extract-s3gcsazure-urls-verify-bucket-exposure`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081088f05f7eb8baeb5d1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

جمع روابط التخزين من ملفات JavaScript وسيلة Recon جيدة. وجود bucket URL لا يثبت أنه عام أو يحتوي بيانات حساسة. تحقق من صلاحيات القراءة والقائمة باستخدام فحوص غير مدمرة وضمن النطاق، ولا تنزّل بيانات مستخدمين أو أسرارًا؛ وثّق أقل دليل كافٍ.

## Payload / Code

```
katana -u [https://target.com](https://target.com) -jc -o js.txt
cat js.txt \| grep -Eo 'https?://\[\^ \]+([s3.amazonaws.com](http://s3.amazonaws.com)\|[storage.googleapis.com](http://storage.googleapis.com)\|[blob.core.windows.net](http://blob.core.windows.net))\[\^ \]\*'
# ثم s3sec أو:
aws s3 ls s3://bucket-name --no-sign-request
```

## Source

Mohamed Ahmed writeup (Mar 2025) + s3sec tool

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
