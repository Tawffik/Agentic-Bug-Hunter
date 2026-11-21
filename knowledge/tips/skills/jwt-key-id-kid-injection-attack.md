# SKILL: JWT: Key ID (kid) Injection Attack

**Skill id:** `tip/jwt-key-id-kid-injection-attack`  
**Category:** Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880814593ccf66cb8e100f2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ kid parameter في الـ JWT header بيقول للسيرفر مفتاح أو ملف التوقيع اللي يستخدمه في التحقق. لو مش متحقق منه كويس، ممكن توجّهه لملف معروف محتواه (زي /dev/null) وتوقّع بنفس المحتوى المعروف ده.

## Payload / Code

```
1) fakk base64 لـ JWT header وpayload
2) عدّل kid → "../../../dev/null"
3) عدّل الـ claims اللي تحتاجها
4) وقّع الـ token بنفس محتوى الملف المعروف كـ secret (مثلاً empty string)
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 25)

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
