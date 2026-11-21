# SKILL: Source Maps → sourcemapper + metis (Intigriti 2026 tip)

**Skill id:** `tip/source-maps-sourcemapper-metis-intigriti-2026-tip`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808156bf0fe9bd66538d71  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Source map (.[js.map](http://js.map)) بيربط JavaScript المضغوط بالكود الأصلي وأسماء الملفات والتعليقات. من الموبايل تقدر تفحصه بالمتصفح فقط: افتح ملف JS من DevTools غير متاح على الموبايل؟ استخدم View Source أو افتح ملفات JS العامة مباشرة، وابحث في آخر الملف عن sourceMappingURL. افتح مسار .map المشار إليه وتأكد أنه يرجع JSON حقيقي وفيه sourcesContent. وجوده وحده غالبًا ليس ثغرة مدفوعة؛ القيمة لما يكشف سرًا حساسًا صالحًا أو مسارًا غير محمي أو منطقًا يؤدي لثغرة أخرى.

## Payload / Code

```
خطوات موبايل بدون تثبيت أدوات: 1) افتح صفحة الهدف المصرح به في Chrome. 2) من قائمة الصفحة اختر عرض المصدر إن كان متاحًا، أو افتح ملفات JS الظاهرة في HTML. 3) ابحث عن sourceMappingURL أو .[js.map](http://js.map). 4) افتح الرابط النسبي الصحيح في المتصفح وتحقق من استجابة JSON ووجود sourcesContent. 5) راجع الكود بحثًا عن endpoints وصلاحيات الواجهة فقط، ولا تستخدم أي token مكشوف. لا تبلّغ عن source map وحده كأنه تسريب بيانات؛ وثّق أثرًا إضافيًا قابلًا للتحقق ضمن النطاق.
```

## Source

[Reeve: Source maps exposed in production (Aug 18, 2026)](https://reeve.page/blog/source-maps-exposed-in-production) ; [BBLabs: Information Disclosure patterns (Apr 2026)](https://bblabs.es/en/academy/basico/information-disclosure-patterns) ; [HackIndex: Source Map Exposure](https://hackindex.io/services/web/vulnerability-discovery/source-map-exposure)

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
