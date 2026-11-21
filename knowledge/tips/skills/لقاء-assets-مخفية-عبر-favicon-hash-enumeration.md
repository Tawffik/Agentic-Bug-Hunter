# SKILL: لقاء Assets مخفية عبر Favicon Hash Enumeration

**Skill id:** `tip/لقاء-assets-مخفية-عبر-favicon-hash-enumeration`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081058374fe65205fd32c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أيقونة الموقع (favicon) ليها hash مميز. لو الشركة بتستخدم نفس الأيقونة في أكتر من host (مثلاً hosts داخلية أو dev servers مفيش لها dns record)، ممكن تلاقيها كلها بالبحث بنفس الـ hash في Shodan/Censys.

## Payload / Code

```
1) استخرج hash الـ favicon بـ Python (mmh3 + base64 favicon.ico)
2) دور بيه في Shodan: http.favicon.hash:\
3) أو في Censys بنفس الـ query
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 3)

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
