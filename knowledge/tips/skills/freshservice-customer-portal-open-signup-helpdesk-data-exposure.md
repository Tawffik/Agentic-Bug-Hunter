# SKILL: Freshservice Customer Portal Open Signup → Helpdesk Data Exposure

**Skill id:** `tip/freshservice-customer-portal-open-signup-helpdesk-data-exposure`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081338f70e26da169db5e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مسار SaaS محدد: بعض مثيلات Freshservice قد تسمح لأي شخص بإنشاء حساب من بوابة الدعم. التسجيل المفتوح وحده ليس ثغرة تلقائيًا؛ الخطر يعتمد على صلاحيات المستخدم الجديد وهل يستطيع رؤية تذاكر أو معلومات داخلية لا ينبغي أن تكون متاحة له. تحقّق من وجود البوابة على نطاق البرنامج ومن صفحة التسجيل العامة فقط. لا تنشئ حسابًا على خدمة حقيقية إلا إذا كانت قواعد البرنامج تسمح صراحة بالتسجيل والاختبار. إذا سمح البرنامج، استخدم حساب اختبار وقيّم فقط المحتوى المخصص لهذا الحساب؛ لا تستعرض تذاكر أو بيانات مستخدمين آخرين. وثّق حدود الوصول والأثر بأقل دليل ممكن.

## Payload / Code

```
مسار مرشح للتحقق: https://\.[freshservice.com/support/signup](http://freshservice.com/support/signup) — لا تعتبر ظهور صفحة التسجيل وحده دليلًا على تسريب بيانات.
```

## Source

Intigriti Misconfig Mapper — Freshworks Freshservice Open User Registration: [https://bugology.intigriti.io/misconfig-mapper-docs/services/freshworks-freshservice/open-user-registration](https://bugology.intigriti.io/misconfig-mapper-docs/services/freshworks-freshservice/open-user-registration) ; Freshworks Support — disable customer portal signups: [https://partnersupport.freshworks.com/en/support/solutions/articles/225287-how-can-i-disable-the-option-for-requesters-to-sign-up-to-our-helpdesk-](https://partnersupport.freshworks.com/en/support/solutions/articles/225287-how-can-i-disable-the-option-for-requesters-to-sign-up-to-our-helpdesk-) ; Research write-up linked by Intigriti: [https://infosecwriteups.com/hundreds-of-companies-internal-data-exposed-part-2-the-freshservice-misconfiguration-a9432c0b5dc8](https://infosecwriteups.com/hundreds-of-companies-internal-data-exposed-part-2-the-freshservice-misconfiguration-a9432c0b5dc8)

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
