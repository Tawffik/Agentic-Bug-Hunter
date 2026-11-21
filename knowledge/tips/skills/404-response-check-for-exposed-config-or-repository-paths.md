# SKILL: 404 response → check for exposed config or repository paths

**Skill id:** `tip/404-response-check-for-exposed-config-or-repository-paths`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081048c3ec0f218c70193  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

صفحة 404 عادية قد تساعد في ملاحظة سلوك routing غير متوقع، لكنها لا تعني أن الملفات بجوارها موجودة. اختبر المسارات الشائعة على أصل الموقع فقط وداخل النطاق، وسجّل status code وحجم الاستجابة ومحتواها. لا تفترض أن حالة المكافأة المذكورة قابلة للتعميم.

## Payload / Code

```
[https://target.com/some/404/path/.git/config](https://target.com/some/404/path/.git/config)
[https://target.com/some/404/path/.env](https://target.com/some/404/path/.env)
```

## Source

InfoSec Write-ups — الرابط الأصلي يحتاج إضافة للتحقق من الحالة المذكورة

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
