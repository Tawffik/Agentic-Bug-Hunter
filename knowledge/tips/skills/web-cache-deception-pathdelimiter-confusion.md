# SKILL: Web Cache Deception — Path/Delimiter Confusion

**Skill id:** `tip/web-cache-deception-pathdelimiter-confusion`  
**Category:** General, XSS  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e0dac31e88081c3a168f78ea9b468e4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General, XSS**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

تحقق هل الـ cache والـ origin يفسران مسار URL بشكل مختلف: قد يصنف الـ cache مسارًا كملف ثابت بينما يعالجه التطبيق كصفحة خاصة. قارن Cache-Control وAge وX-Cache واختبر فقط بمحتوى تجريبي غير حساس داخل حسابك. لا تحاول تخزين أو استرجاع صفحات خاصة لمستخدمين آخرين؛ الأثر يتطلب إثبات أن استجابة حساسة قابلة للتخزين والمشاركة.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Professor the Hunter — 07 Sep 2023 (رابط المنشور الأصلي غير متاح في السجل الحالي). مرجع تعليمي مكمل: PortSwigger — Web cache deception: [https://portswigger.net/web-security/web-cache-deception](https://portswigger.net/web-security/web-cache-deception)

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
