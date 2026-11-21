# SKILL: Symfony Profiler / app\_dev.php Exposed → Debug Trace & Environment Disclosure

**Skill id:** `tip/symfony-profiler-app-devphp-exposed-debug-trace-environment-disclosure`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081058430e008be1450f9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مسار خاص بتطبيقات Symfony: ابحث عن دلائل Symfony في HTML أو response headers، ثم راجع إن كانت واجهة profiler أو مسارات التطوير متاحة على production. وجود /\_profiler أو app\_dev.php كاسم مسار وحده لا يثبت ثغرة؛ الدليل هو وصول غير مصرح به إلى traces أو تفاصيل البيئة أو الاستثناءات أو بيانات الطلب. استخدم طلبًا محدودًا وقارن دون تسجيل الدخول وبحساب اختبار؛ إذا ظهر محتوى حساس توقف ولا تستعرض بقية السجلات. دوّن فقط نوع المعلومات بعد تنقيح القيم السرية، وتأكد أن الأصل ضمن النطاق.

## Payload / Code

```
مسارات مرشحة للتحقق فقط عند وجود بصمة Symfony: /\_profiler و/app\_dev.php/\_profiler — لا تعتبر status 200 وحده إثباتًا.
```

## Source

Intigriti Misconfig Mapper — Symfony Profiler Enabled: [https://bugology.intigriti.io/misconfig-mapper-docs/services/symfony-php/symfony-profiler-enabled](https://bugology.intigriti.io/misconfig-mapper-docs/services/symfony-php/symfony-profiler-enabled) ; Symfony Profiler documentation: [https://symfony.com/doc/current/profiler.html](https://symfony.com/doc/current/profiler.html) ; Intigriti Misconfig Mapper supported services: [https://bugology.intigriti.io/misconfig-mapper-docs/readme/services](https://bugology.intigriti.io/misconfig-mapper-docs/readme/services)

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
