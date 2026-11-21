# SKILL: Fat GET Requests — تمرير Params في الـ Body لتجاوز Cache Key

**Skill id:** `tip/fat-get-requests-تمرير-params-في-الـ-body-لتجاوز-cache-key`  
**Category:** WAF Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/8abceb05f39443978e343f981e3141b5  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض السيرفرات (خصوصًا Ruby/PHP/بعض الـ frameworks) بتقرا الباراميترات من body بتاع ريكوست GET كمان. الكاش بيعمل الـ cache key على الـ URL/query فقط ومبيشوفش الـ body، فالقيمة اللي في الـ body تعتبر unkeyed input. ده بيديك مدخل مخفي تسمّم بيه الكاش أو تتجاوز فلاتر الـ WAF اللي بتفحص الـ query string بس.

## Payload / Code

```
GET /search?q=test HTTP/1.1
Host: [target.com](http://target.com)
Content-Length: 24

q=\alert(1)\
// بعض الـ frameworks بتقرا الـ params من body الـ GET، بينما الكاش بيعمل key على query string بس
```

## Source

SecurityCipher — Web Cache Poisoning Playbook 2026

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
