# SKILL: IDOR Chaining — تسريب Email من Profile + Password Reset = ATO

**Skill id:** `tip/idor-chaining-تسريب-email-من-profile-password-reset-ato`  
**Category:** IDOR, Auth Bypass, Password Reset  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/5fbf2db9ceb54a10a93adef4d49c4114  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Auth Bypass, Password Reset**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

IDOR على GET لوحده = تسريب معلومات بس (غالبًا Medium). القوة الحقيقية في التشيين: تستخدم الـ IDOR عشان تطلّع email/UUID بتاع الضحية، وبعدها تستغلّه في password reset أو في ربط حسابك ببياناته = Account Takeover كامل (Critical). دايمًا اسأل نفسك: الـ leak ده ممكن يتحوّل لإيه أكبر؟

## Payload / Code

```
GET /api/v2/users?id=victim\_id   // يرجّع email/PII بتاع الضحية
// جرّب لما endpoint /users/victim\_id يرد 401، بدّله لـ ?id=victim\_id
// بعدها: password reset على الـ email اللي طلع، أو اربط الحسابين
```

## Source

BBLabs / Foysal Ahmed — \$4500 IDOR to ATO 2025

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
