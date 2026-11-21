# SKILL: Source maps (.[js.map](http://js.map)) → full frontend source + secrets

**Skill id:** `tip/source-maps-jsmaphttpjsmap-full-frontend-source-secrets`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081f28c0dcafe47e2e8a4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Source map (.[js.map](http://js.map)) بيرجع خريطة من الكود المضغوط للكود الأصلي للواجهة، وقد يكشف أسماء ملفات ومسارات API وتعليقات ومنطق الواجهة. تقدر تعمل فحص أولي من موبايلك بالمتصفح فقط عبر فتح ملفات JS العامة والبحث عن sourceMappingURL ثم تجربة رابط .map المشار إليه. مجرد ظهور الكود الأصلي ليس دليلًا كافيًا على أثر أمني؛ لازم تلاقي سرًا حساسًا صالحًا أو endpoint/صلاحية تؤدي إلى وصول غير مصرح به، ومن غير استخدام مفاتيح مسربة أو لمس بيانات ناس.

## Payload / Code

```
Mobile-only check: افتح HTML/JS العام للهدف المصرح به، ابحث عن sourceMappingURL، وافتح ملف .map المشار إليه. تأكد أنه JSON فعلي وليس مجرد تعليق في JS. افحص أسماء endpoints والمنطق الظاهر فقط. لا تستخدم credential أو token مكشوف ولا تنزّل بيانات مستخدمين. أوقف الاختبار عند إثبات الحد الأدنى من الأثر.
```

## Source

[Reeve: Source maps exposed in production (Aug 18, 2026)](https://reeve.page/blog/source-maps-exposed-in-production) ; [BBLabs: Information Disclosure patterns](https://bblabs.es/en/academy/basico/information-disclosure-patterns) ; [HackIndex: Source Map Exposure](https://hackindex.io/services/web/vulnerability-discovery/source-map-exposure)

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
