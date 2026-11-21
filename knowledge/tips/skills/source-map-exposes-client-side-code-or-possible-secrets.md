# SKILL: Source map exposes client-side code or possible secrets

**Skill id:** `tip/source-map-exposes-client-side-code-or-possible-secrets`  
**Category:** Recon, API Hacking  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880810fb64fceeae9e140e4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ملف source map قد يكشف الكود الأصلي، لكنه لا يثبت وحده وجود مفتاح Stripe صالح أو أثر مالي. لا ترسل مفاتيح مكتشفة إلى API لاختبار صلاحيتها أو قراءة بيانات الحساب. تحقق من السياق محليًا، واحجب القيمة في التقرير، واستخدم دليلًا عامًا أو تنسيق المفتاح فقط ما لم يسمح البرنامج صراحةً باختبار آمن.

## Payload / Code

```
sourcemapper -url [https://target.com/static/js/main.js.map](https://target.com/static/js/main.js.map) -output ./src
# ابحث عن sk\_live\_ أو pk\_live\_
curl [https://api.stripe.com/v1/balance](https://api.stripe.com/v1/balance) -u sk\_live\_XXXX:
```

## Source

ProDefense / Matthew Keeley writeup – \$25k paid

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
