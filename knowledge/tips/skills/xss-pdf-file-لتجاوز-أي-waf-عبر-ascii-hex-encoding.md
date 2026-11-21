# SKILL: XSS: PDF file لتجاوز أي WAF عبر ASCII hex encoding

**Skill id:** `tip/xss-pdf-file-لتجاوز-أي-waf-عبر-ascii-hex-encoding`  
**Category:** XSS, WAF Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081bbaf14fbea1f8cf349  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو لاقي Stored XSS لكن الـ WAF بيبلع الـ payload العادي، اعمل encode للـ payload كـ ASCII hex (ممكن تعدّله براحتك في Notepad++) قبل ما ترفعه. التقنية دي قابلة للتطوير لـ Blind XSS كمان.

## Payload / Code

```
1) اكتب الـ XSS payload العادي
2) عمله encode كـ ASCII hex
3) عدّل الـ payload المشفر في Notepad++ لو احتجت
4) ارفعه في مكان الـ upload/input اللي خلف الـ WAF
```

## Source

kjulius @ethical\_h4ck3r\_ — Credit: @GodfatherOrwa

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
