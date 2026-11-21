# SKILL: MQTT / WebSocket Chat Backend — Topic Authorization & Cross-Session Disclosure

**Skill id:** `tip/mqtt-websocket-chat-backend-topic-authorization-cross-session-disclosure`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081629442f99133c6f479  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

فكرة متخصصة مش مغطاة بوضوح في صفحة WebSocket العامة: بعض تطبيقات الدعم الحي تكشف في JavaScript عنوان chat backend أو ملف إعدادات مثل env\_app.js، ثم تتصل بخدمة MQTT عبر WebSocket. وجود الإعدادات علنًا ليس ثغرة بحد ذاته؛ نقطة الاختبار هي هل المصادقة وعزل الـ topics يضمنان أن حساب الاختبار لا يستطيع الوصول إلا إلى جلساته. راجع ملفات JS العامة على أصل داخل النطاق، سجّل أسماء البروتوكولات والـ host فقط، ثم تحقق بحسابين تملكهما وجلسات اختبارية. لا تستخدم اشتراكات واسعة لجمع رسائل عملاء حقيقيين، ولا تحتفظ ببياناتهم؛ أوقف الاختبار فور ظهور بيانات لا تخص حساباتك. التقرير القوي يثبت خلط جلسات بين حسابين تجريبيين فقط.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Mahbubur Rahman Soraf (2026-06-03): [https://medium.com/%40lazysharaf/how-i-hacked-a-live-chatbot-and-earned-my-first-4-digit-bounty-5c43c8891741](https://medium.com/%40lazysharaf/how-i-hacked-a-live-chatbot-and-earned-my-first-4-digit-bounty-5c43c8891741) ; Intigriti Bug Bytes #229: [https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-229-october-2025](https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-229-october-2025) ; OWASP WebSocket Security Cheat Sheet: [https://cheatsheetseries.owasp.org/cheatsheets/WebSocket\_Security\_Cheat\_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html)

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
