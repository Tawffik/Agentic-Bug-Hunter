# SKILL: Laravel Telescope in Production → Request / Query / Exception Disclosure

**Skill id:** `tip/laravel-telescope-in-production-request-query-exception-disclosure`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880816a9699c2cca7602563  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

فحص متخصص لتطبيقات Laravel: وجود Telescope وحده لا يثبت الثغرة؛ الإشارة المهمة هي أن واجهة Telescope أو سجلات الطلبات/الاستثناءات يمكن قراءتها من دور غير مخول. قد تحتوي البيانات على مسارات داخلية أو تفاصيل طلبات أو استعلامات أو قيم حساسة. ابدأ بطلب محدود للواجهة المعروفة، وقارن استجابة غير مسجل الدخول بحساب اختبار عادي. لا تتصفح سجلات فعلية إذا ظهر محتوى غير مخصص لك؛ وثّق نوع البيانات مع إخفاء الأسرار. لا تختبر إلا على أصل داخل النطاق.

## Payload / Code

```
مسار مرشح للتحقق: /telescope/requests — نتيجة HTTP 200 وحدها ليست إثباتًا؛ راجع محتوى الاستجابة وحدود الوصول.
```

## Source

Intigriti Misconfig Mapper (official repository templates): [https://github.com/intigriti/misconfig-mapper/blob/main/templates/services.json](https://github.com/intigriti/misconfig-mapper/blob/main/templates/services.json) ; Laravel Telescope documentation: [https://laravel.com/docs/12.x/telescope](https://laravel.com/docs/12.x/telescope) ; Intigriti Misconfig Mapper project: [https://github.com/intigriti/misconfig-mapper](https://github.com/intigriti/misconfig-mapper)

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
