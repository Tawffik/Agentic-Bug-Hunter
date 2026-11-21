# SKILL: Business Logic: Bypass الأسعار بتلاعب العملات (Currency Confusion)

**Skill id:** `tip/business-logic-bypass-الأسعار-بتلاعب-العملات-currency-confusion`  
**Category:** General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880811f81cbcbd7cf289ce1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الأنظمة اللي بتتعامل مع أكتر من عملة بتستخدم exchange rate function. لو مفيش تحقق كويس، جرّب تغيّر العملة لعملة أضعف (زي INR أو JPY) وشوف هل السعر النهائي بيتحسب صح ولا لأ — ممكن تشتري بسعر أقل بكتير من قيمة المنتج الحقيقية.

## Payload / Code

```
لو فيه param اسمه currency أو lang بيتحكم في الـ pricing، جرّب:
currency=INR بدل currency=USD (مع نفس السعر الرقمي)
وشوف هل السيرفر بيحول العملة صح أو لأ
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 20)

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
