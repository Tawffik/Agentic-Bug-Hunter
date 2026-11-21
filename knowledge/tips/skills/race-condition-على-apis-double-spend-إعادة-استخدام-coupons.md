# SKILL: Race Condition على APIs — Double Spend / إعادة استخدام Coupons

**Skill id:** `tip/race-condition-على-apis-double-spend-إعادة-استخدام-coupons`  
**Category:** API Hacking, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/676052a8958c4a50b1598eccf314f4b0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الـ endpoint بيعمل check ثم action في خطوتين منفصلين من غير lock/transaction، تقدر تبعت كثير ريكوست في نفس اللحظة (single-packet attack) فتعدي كلها الـ check قبل ما الـ state يتحدّث. النتيجة: تصرف فلوس أكتر من رصيدك، تستخدم كوبون مرات كتيرة، تتجاوز rate limit، أو تعمل مليار دعوة. من أعلى الثغرات ربحًا حاليًا.

## Payload / Code

```
// Burp Repeater → Create tab group → Send group in parallel (single-packet attack)
// أو Turbo Intruder بـ [race-single-packet-attack.py](http://race-single-packet-attack.py)
// ابعت 20-50 ريكوست متزامنين لـ: redeem coupon / withdraw / transfer / vote / claim
```

## Source

PortSwigger Research (Single-Packet Attack) / vux06 BB-Methodology

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
