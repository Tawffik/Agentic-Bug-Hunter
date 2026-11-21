# SKILL: IDOR: منهجية احترافية بأداة Authz + Burp Intruder

**Skill id:** `tip/idor-منهجية-احترافية-بأداة-authz-burp-intruder`  
**Category:** IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081a3bde1e1f9f284aa70  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أداة Authz extension في Burp بتخليك تحط session token لمستخدم تاني (victim) وتقارن automatically أي فرق في الـ response لما تصفح كـ User A. للـ IDs الرقمية استخدم Burp Intruder برينج رقمي وابحث عن كلمات زي email/address/total في الردود.

## Payload / Code

```
1) تصفح كـ User A وسجّل كل request فيه object identifier
2) أدخل session token بتاع User B في Authz extension
3) قارن automatically content-length/status code

للـ numeric IDs في Intruder:
GET /api/v1/invoices/§1001§ HTTP/1.1
Authorization: Bearer \
(رانج 1000-1100 وافحص ردود فيها email/address/total)

للـ UUIDs: استخدم Turbo Intruder مع قائمة UUIDs ملقوطة من endpoints تانية
```

## Source

Redfox Security 2026

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
