# SKILL: 🗺️ Source Map Pivot — app.js → [app.js.map](http://app.js.map) → original routes/hosts/comments

**Skill id:** `tip/source-map-pivot-appjs-appjsmaphttpappjsmap-original-routeshostscomments`  
**Category:** Recon, XSS, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e8808103b19ed81708146554  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, XSS, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: source map قد يعيد أسماء الملفات الأصلية وroutes وhostnames وcomments وأحيانًا sourcesContent.

workflow:
JS asset → candidate .map → validate map → extract sources/sourceRoot/sourcesContent → URLs/hosts/routes/secrets candidates → current validation.

مهم: وجود source map ليس تلقائيًا vulnerability. القيمة تأتي من data exposed + current relation + impact.

## Payload / Code

```
app.js
→ [app.js.map](http://app.js.map)
→ sourcesContent
→ routes/hosts/config
→ current validation
```

## Source

Bug bounty client-side/source-map research patterns

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
