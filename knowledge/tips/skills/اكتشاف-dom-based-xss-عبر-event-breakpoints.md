# SKILL: اكتشاف DOM-based XSS عبر Event Breakpoints

**Skill id:** `tip/اكتشاف-dom-based-xss-عبر-event-breakpoints`  
**Category:** XSS  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808135afc7e4ad592eeeb2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ DOM XSS صعبة تلاقيها لأنها مش بتظهر في الـ response العادي. استخدم developer console وحط event breakpoints على DOM sinks (innerHTML, document.write, eval) عشان تتتبع هل الـ input بتاعك بيوصل لهم بدون sanitization. أداة DOM Invader المدمجة في Burp بتعمل ده أوتوماتيكيًا.

## Payload / Code

```
1) Sources tab في Chrome DevTools
2) حط event breakpoint على DOM sinks
3) حلل هل input مباشر بيوصل للـ sink

مثال للـ sink pattern: document.getElementById("output").innerHTML = new URLSearchParams([location.search](http://location.search)).get("msg");
```

## Source

Intigriti Official 2026 (Tip 14) + Redfox Security 2026

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
