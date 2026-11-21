# SKILL: Web Cache Deception → تحويل Reflected XSS إلى Stored

**Skill id:** `tip/web-cache-deception-تحويل-reflected-xss-إلى-stored`  
**Category:** XSS, WAF Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/b5a9dc0fb648421db2eb5869e871f6a4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة إن الـ CDN/Cache بيكاش أي URL شكله static (بينتهي بـ .css/.js). لو قدرت تخلي صفحة فيها بيانات حساسة أو reflected XSS تترد على URL بامتداد static، الكاش هيخزّن الرد ويقدّمه لأي زائر. كده بتحوّل Reflected XSS (مؤقت) لـ Stored XSS بيضرب كل الضحايا بريكوست واحد، أو بتسرّب بيانات مستخدمين تانيين المكاشة.

## Payload / Code

```
[https://target.com/account.php/nonexistent.css](https://target.com/account.php/nonexistent.css)
[https://target.com/api/me%0a.css](https://target.com/api/me%0a.css)
[https://target.com/profile;.js](https://target.com/profile;.js)
// جرّب امتدادات static (.css/.js/.jpg) + path confusion + encoded delimiters (%2f %00 ;)
```

## Source

SecurityCipher / PortSwigger Research — Web Cache Deception 2026

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
