# SKILL: 🔁 Metadata Flow — Referer/Origin/Redirect قد يسرّب Identifier حساس

**Skill id:** `tip/metadata-flow-refereroriginredirect-قد-يسرّب-identifier-حساس`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e8808174a898c72179103fff  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: التسريب قد يحصل أثناء انتقال البيانات بين requests، وليس داخل response body فقط.

راجع:
Referer / Origin / Location / redirect chain / Cookie / Referrer-Policy / CSP.

الـpattern:
sensitive identifier → navigation/request → cross-origin boundary → identifier يظهر في metadata.

مثال حقيقي: HackerOne disclosed Brave report عن Information Disclosure عبر Referer leak.

مهم: Referer موجود طبيعيًا في كثير من المواقع؛ finding يتطلب إثبات أن data حساسة عبرت boundary غير مقصودة.

## Payload / Code

```
URL
→ redirect/navigation
→ Referer/Origin
→ external boundary
→ sensitive identifier?
```

## Source

HackerOne disclosed Brave report — Referer leak

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
