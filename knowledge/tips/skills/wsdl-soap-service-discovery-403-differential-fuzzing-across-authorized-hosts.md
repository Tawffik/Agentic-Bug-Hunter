# SKILL: WSDL / SOAP Service Discovery + 403 Differential Fuzzing Across Authorized Hosts

**Skill id:** `tip/wsdl-soap-service-discovery-403-differential-fuzzing-across-authorized-hosts`  
**Category:** Fuzzing, Recon, API Hacking, WAF Bypass  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e88081c4a4a6f5a8dc8815a7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing, Recon, API Hacking, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: لو endpoint بيرجع 403، ما تعتبرش ده نهاية الاختبار ولا دليل على وجود ثغرة. في الخدمات القديمة أو المؤسسية، افحص هل الخدمة SOAP وهل وصفها متاح عبر WSDL، ثم قارن سلوك الـ endpoint على الدومينات والـ virtual hosts المصرح بها. اختلاف الاستجابة قد يكشف إعدادات غير متسقة أو سطح API قديم، لكنه لا يثبت تجاوز صلاحيات وحده.

## Payload / Code

```
أمثلة آمنة على صيغة المسارات للفحص داخل النطاق المصرح فقط:
- /service?wsdl
- /service?WSDL
- /service.wsdl

اختبر GET أولًا، ثم قارن OPTIONS أو HEAD عند ملاءمتها وضمن قواعد البرنامج. سجّل status code وLocation وContent-Type وحجم/بصمة الاستجابة. قارن بين hostnames المصرح بها فقط مع إبقاء المسار والطلب ثابتين. لا ترسل SOAP operations تغيّر بيانات أو تنفّذ إجراءات.
```

## Source

Screenshot shared by user — Abdulrhman A Saad; original post URL not visible in screenshot

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
