# SKILL: Web cache poisoning via malformed Cookie parameter

**Skill id:** `tip/web-cache-poisoning-via-malformed-cookie-parameter`  
**Category:** API Hacking, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808197b36fd55b0d3bec54  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الـcaches تُدخل قيم Cookie غير صالحة في مفتاح الكاش أو تتعامل معها بشكل مختلف عن origin. جرّب Cookie مشوّه/مكرر/بقيم خاصة وراقب Cache-Control وVary وX-Cache وهل المحتوى المسموم يُخدم لمستخدم آخر. التأثير الحقيقي = تسميم استجابة مشتركة لمستخدمين آخرين، مش اختلاف رد لنفسك فقط.

## Payload / Code

```
Try malformed Cookie shapes (authorized targets):
Cookie: =
Cookie: name=
Cookie: name=""
Cookie: ;;;;;;;;
Cookie: a=b
Compare responses + cache headers between poisoned and clean clients.
Confirm unauthenticated victim receives poisoned page before reporting.
```

## Source

kassem \$1500 cache poisoning tip (X)

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
