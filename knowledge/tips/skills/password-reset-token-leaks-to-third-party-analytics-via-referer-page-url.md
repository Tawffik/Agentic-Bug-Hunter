# SKILL: Password-reset token leaks to third-party analytics via Referer / page URL

**Skill id:** `tip/password-reset-token-leaks-to-third-party-analytics-via-referer-page-url`  
**Category:** Auth Bypass, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880813c950ae2c0a96b030e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعد فتح رابط إعادة التعيين، قد تحتوي الصفحة أو عنوان URL على token ثم تُحمّل analytics أو صورًا أو سكربتات من طرف ثالث. افحص هل الرابط الحساس أو token ينتقل في Referer أو سجلات الطرف الثالث، وهل يتم استهلاكه لمرة واحدة وبصلاحية قصيرة. استخدم حسابك الاختباري وتوكنًا تملكه فقط، ولا تجمع توكنات مستخدمين آخرين. وجود Referer وحده لا يكفي؛ المطلوب إثبات وصول السر إلى جهة غير موثوقة.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

HackerOne Report #4000185: [https://hackerone.com/reports/4000185](https://hackerone.com/reports/4000185) ; PortSwigger — Password reset poisoning: [https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning)

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
