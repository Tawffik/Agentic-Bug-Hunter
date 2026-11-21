# SKILL: XSS: تشفير كلمة javascript: بـ HTML Entities لتجاوز الفلاتر

**Skill id:** `tip/xss-تشفير-كلمة-javascript-بـ-html-entities-لتجاوز-الفلاتر`  
**Category:** XSS, WAF Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081db94d7c17862d420e7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

استخدام HTML entity encoding (decimal مع hex) جوه كلمة javascript عشان تتجاوز فلاتر بتدور على الكلمة العادية "javascript:" في الـ URL params اللي بتتحط لـ redirect أو href.

## Payload / Code

```
url=%26%2302java%26%23115cript:alert(document.domain)
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
