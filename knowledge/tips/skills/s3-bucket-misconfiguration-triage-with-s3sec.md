# SKILL: S3 bucket misconfiguration triage with s3sec

**Skill id:** `tip/s3-bucket-misconfiguration-triage-with-s3sec`  
**Category:** Recon  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081808084c609234d95ae  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

استخدم s3sec كأداة تحقق موجهة على Buckets مرتبطة بأصول داخل نطاق البرنامج. ابدأ بتحديد الـ bucket من ملفات JS أو مصادر recon، ثم افحص الصلاحيات بأقل طلبات ممكنة. فرّق بين listing/read/write/delete؛ لا ترفع أو تحذف ملفات ولا تختبر بيانات مستخدمين. سجّل الدليل الآمن واسم الـ bucket والـ policy الظاهرة، وتوقف إذا ظهر محتوى حساس.

## Payload / Code

```
Tool: s3sec — لم أتمكن من تأكيد رابط المستودع الأصلي من المصدر المرسل، لذلك لم أضع رابطًا تخمينيًا. أضف رابط المصدر الصحيح قبل التشغيل.
Checklist: scope → identify bucket → inspect permissions → minimal proof → redact sensitive data.
```

## Source

User-provided collection: s3sec S3 read/write/delete permission checker; verify exact repository URL before use.

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
