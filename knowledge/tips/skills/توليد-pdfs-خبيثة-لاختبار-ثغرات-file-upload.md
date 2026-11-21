# SKILL: توليد PDFs خبيثة لاختبار ثغرات File Upload

**Skill id:** `tip/توليد-pdfs-خبيثة-لاختبار-ثغرات-file-upload`  
**Category:** General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081c083c2c4ed3e088bc2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما تدور على web shells وصور بس، الـ PDFs ممكن تسبب مشاكل في الـ server-side rendering زي SSRF وXSS وحتى RCE لو الأبلكيشن بيعمل process للـ PDF بطريقة غير آمنة (مثلاً conversion libraries فيها ثغرات).

## Payload / Code

```
استخدم أداة توليد payloads PDF تختبر SSRF/XSS/RCE مع callback URL خاص بيك، ثم ارفعها في أي مكان بيقبل رفع/معالجة PDF
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 18)

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
