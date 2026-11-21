# SKILL: MFA flow validation: test for server-side enforcement

**Skill id:** `tip/mfa-flow-validation-test-for-server-side-enforcement`  
**Category:** Auth Bypass  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808131b897da55a3b4906b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اختلاف أسماء endpoints لا يعني وجود مسار لتجاوز MFA. راجع تدفق المصادقة في حساب اختبار تملكه، وتحقق هل الخادم يرفض الوصول المحمي قبل إتمام MFA. لا تتخطَّ عامل المصادقة لحساب شخص آخر، ولا تعتمد أسماء مسارات تخمينية كـ payload عام.

## Payload / Code

```
POST /mfa/skip  (بدل /mfa/verify)
```

## Source

farhaan Medium writeup – \$10,000 bounty

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
