# SKILL: 🪟 JS Global Surface — لا تبحث فقط عن API URLs؛ فتّش عن Window Globals وHandlers

**Skill id:** `tip/js-global-surface-لا-تبحث-فقط-عن-api-urls؛-فتّش-عن-window-globals-وhandlers`  
**Category:** Recon, XSS, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e880810fb49df611cb258aa6  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, XSS, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: JavaScript قد يكشف security-relevant interfaces عبر globals أو event handlers وليس secrets فقط.

فتّش عن:
window.*, custom globals, postMessage handlers, custom events, client-side tokens, browser/extension APIs.

مثال حقيقي: تقرير Brave منشور عن security token وhandler name متاحين من window.braveBlockRequests وحصل على bounty.

الـpivot: global/handler → identify producer/consumer → determine whether data crosses a security boundary.

## Payload / Code

```
window.\*
postMessage
message handlers
custom events
client-side tokens
```

## Source

HackerOne disclosed Brave reports — client-side token/handler information disclosure

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
