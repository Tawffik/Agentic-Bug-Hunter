# SKILL: Recon شامل: HTTP Methods/Headers Fuzzing + Path Fuzzing

**Skill id:** `tip/recon-شامل-http-methodsheaders-fuzzing-path-fuzzing`  
**Category:** Fuzzing, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081d4bc34e4a5dfdb4769  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

تجربة methods وheaders وpaths مختلفة ممكن تكشف صفحات أو سلوكيات مخفية أو تتجاوز قيود الوصول (access control) المبنية على شرط بسيط في السيرفر.

## Payload / Code

```
HTTP Methods fuzzing: GET, POST, TRACE, HEAD...
HTTP Headers fuzzing: X-Originating-IP: 127.0.0.1, X-Forwarded-For: 127.0.0.1...
Path fuzzing / force browsing: /admin/[index.ht](http://index.ht).., /admin/./index...
Protocol version changing: HTTP/1.2 downgrade لـ HTTP/1.1
String terminators: %00, 0x00, //, ; %12 ...الخ (تتضاف في آخر الـ path)
```

## Source

Ali @darkyfy

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
