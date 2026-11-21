# SKILL: منطق SQL Injection: أولوية AND قبل OR (شرح تفصيلي)

**Skill id:** `tip/منطق-sql-injection-أولوية-and-قبل-or-شرح-تفصيلي`  
**Category:** SQLi, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081f98469c45068fccb5c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ AND أعلى أولوية من الـ OR في SQL. الطرف الشمال (username AND password) بيبقى False لو الباسورد غلط، لكن الطرف اليمين ('1'='1') مقارنة بين رقمين ثابتين دايمًا True، ومفيهاش أي عمود في الجدول. النتيجة: False OR True = True لكل صف في الجدول، يعني الشرط بيرجع الجدول كله. غالبًا أول صف في جدول الـ logins بيكون الـ admin (لأنه أول حساب اتعمل بـ id=1)، فبيتم تسجيل الدخول كـ admin من غير ما تعرف الباسورد بتاعه.

## Payload / Code

```
WHERE (username='tom' AND password='') OR ('1'='1')

مثال تنفيذي:
SELECT \* FROM logins WHERE username='tom' AND password = '' OR '1' = '1';
→ Login successful as user: admin
```

## Source

لقطة شاشة شرح شخصي عربي (تجربة على Hack The Box)

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
