# SKILL: أداة Reflix: اكتشاف باراميترات ورصد DOM XSS sinks أوتوماتيكيًا

**Skill id:** `tip/أداة-reflix-اكتشاف-باراميترات-ورصد-dom-xss-sinks-أوتوماتيكيًا`  
**Category:** XSS, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808112836df7ef2c84072c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أداة opensource بتعمل parameter discovery + reflection fuzzing (في query وpath وheaders) وبتحدد أماكن DOM XSS sinks مع رقم السطر بالظبط، بدل ما تدور فزّينج يدوي أو تدور على Burp لوحده.

## Payload / Code

```
الأداة: Reflix
repo: [github.com/nexovir/reflix](http://github.com/nexovir/reflix)
الاستخدام: python3 [reflix.py](http://reflix.py) -d urls.txt (parameter discovery + reflection fuzzing)
```

## Source

Radvan Mohamadzade @nexovir

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
