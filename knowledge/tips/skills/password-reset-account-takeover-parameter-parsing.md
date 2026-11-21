# SKILL: Password Reset → Account Takeover — Parameter Parsing

**Skill id:** `tip/password-reset-account-takeover-parameter-parsing`  
**Category:** Password Reset, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e0dac31e880812ba8bdc4d82c440a36  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اختبر في حسابات تملكها هل endpoint إعادة التعيين يفسر البريد أو المستخدم أو redirect بطريقة مختلفة عن الواجهة، خصوصًا مع تكرار الباراميتر أو اختلاف ترتيب القيم. راقب أي اختلاف في الرسالة أو وجهة البريد، ولا تعتبره ATO إلا إذا أثبتت أن العملية تربط الرمز بالحساب الصحيح وأنه لا يمكن استخدامه على حساب آخر. استخدم بريدين اختباريين تملكهما فقط.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Professor the Hunter — 24 Nov 2025 (رابط المنشور الأصلي غير متاح في السجل الحالي). مرجع رسمي مكمل: PortSwigger — Password reset poisoning: [https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning)

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
