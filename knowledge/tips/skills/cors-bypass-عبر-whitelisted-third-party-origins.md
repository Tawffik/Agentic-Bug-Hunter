# SKILL: CORS Bypass عبر Whitelisted Third-Party Origins

**Skill id:** `tip/cors-bypass-عبر-whitelisted-third-party-origins`  
**Category:** CSRF, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081e687bdf6c7ef45a150  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **CSRF, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الأنظمة بتعمل whitelist لـ domains زي GitHub Pages, CodePen, Replit للتطوير لكن بتنسى تشيلهم في Production. استضيف الـ PoC بتاعك على أي من الـ domains دي واعمل cross-origin request تتجاوز CORS لأنها موثوقة.

## Payload / Code

```
1) افحص Access-Control-Allow-Origin في الـ response headers
2) لو فيه domains زي \*.[github.io](http://github.io) أو [codepen.io](http://codepen.io) مسموحة
3) استضيف fetch() PoC على نفس الـ domain ده واسحب البيانات
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 31)

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
