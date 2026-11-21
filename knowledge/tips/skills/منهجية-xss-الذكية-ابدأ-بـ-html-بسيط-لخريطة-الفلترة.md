# SKILL: منهجية XSS الذكية — ابدأ بـ HTML بسيط لخريطة الفلترة

**Skill id:** `tip/منهجية-xss-الذكية-ابدأ-بـ-html-بسيط-لخريطة-الفلترة`  
**Category:** XSS, WAF Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/2565f31078e8494d8de178883e472dab  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما ترمي polyglot payloads عشوائية على كل حقل (وده بيتبلّك بسرعة ويتكرر)، ابدأ بـ tags بسيطة جدًا عشان تفهم الـ context (HTML؟ attribute؟ JS؟) وإيه اللي الـ filter بيسمح بيه. لما تفهم الفلترة بتمنع إيه، تقدر تبني payload دقيق يتجاوزها بدل التخمين. XSS لسة \~18% من الـ valid submissions.

## Payload / Code

```
1) ابدأ بـ: test123\xss\   // هل الـ tags بتترندر؟
2) لو آه: ">\x   // هل تقدر تخرج من attribute/context؟
3) بعدها بس: event handlers و payloads حقيقية حسب الـ context
// متبدأش بـ polyglots عشوائي
```

## Source

NahamSec — Advanced XSS Methodology 2025

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
