# SKILL: HTTP Request Smuggling — CL.TE / [TE.CL](http://TE.CL) + HTTP/2 Downgrade

**Skill id:** `tip/http-request-smuggling-clte-teclhttptecl-http2-downgrade`  
**Category:** WAF Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/0fd8610fcf8a4bc283612bb93e06e3f5  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أغلب ثغرات الـ high-severity الحقيقية هي اختلافات في parsing الـ HTTP بين الـ front-end والـ back-end. لو الاثنين بيختلفوا في تفسير Content-Length ضد Transfer-Encoding (أو في HTTP/2 downgrade)، تقدر تهرّب ريكوست جوّا ريكوست، فتسمّم الكاش، تخطف ريكوستات مستخدمين تانيين، أو تتجاوز ضوابط الأمان والـ WAF. استخدم HTTP Request Smuggler للكشف الأولي.

## Payload / Code

```
# Burp → HTTP Request Smuggler extension (Detect)
# CL.TE mismatch:
Content-Length: 6
Transfer-Encoding: chunked

0

G
# HTTP/2 downgrade: جرّب [h2.CL](http://h2.CL) / h2.TE و CRLF جوّا الـ headers
```

## Source

PortSwigger Research / HuntBook 2026

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
