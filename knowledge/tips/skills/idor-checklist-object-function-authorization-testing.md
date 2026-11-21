# SKILL: IDOR Checklist — Object & Function Authorization Testing

**Skill id:** `tip/idor-checklist-object-function-authorization-testing`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e0dac31e880817b886ccf490b78a1a1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أنشئ مصفوفة بسيطة بحسابين تملكهما: مالك المورد، مستخدم آخر، وأدوار مختلفة إن وجدت. اختبر القراءة والتعديل والحذف والعمليات الإدارية كلًا على حدة؛ لا تفترض أن حماية GET تعني حماية PATCH/DELETE أو أن UUID يمنع الوصول. سجل الطلب والاستجابة والأثر الأدنى اللازم، ولا تفتح بيانات مستخدمين حقيقيين.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Professor the Hunter — 29 Oct 2025 (رابط المنشور الأصلي غير متاح في السجل الحالي). مرجع رسمي مكمل: OWASP API Security — Broken Object Level Authorization: [https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

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
