# SKILL: JWT: هجوم 'None' Algorithm — Bypass Authentication

**Skill id:** `tip/jwt-هجوم-none-algorithm-bypass-authentication`  
**Category:** Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081749e28f18c2aa5de16  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض أنظمة JWT قديمة بتقبل الـ algorithm 'none' يعني مفيش أي signature verification. لو عدّلت الـ header وشلت الـ signature وسيبت الـ alg مساوي none، السيرفر ممكن يقبل الـ token المزور بدون ما يفشل.

## Payload / Code

```
1) fakk base64 لـ JWT header وpayload
2) غيّر "alg": "HS256" → "alg": "none"
3) عدّل الـ claims (مثلاً role: admin)
4) شيل الـ signature خالص لكن افضل الـ dot في الآخر (header.payload.)

استخدم JWT Editor Extension في Burp للتسهيل
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 24)

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
