# SKILL: 🧬 Error Grammar → Technology → Targeted Pivot

**Skill id:** `tip/error-grammar-technology-targeted-pivot`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081fbb961cd5c79147c79  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: لا تحفظ 500 كرقم فقط. حلّل لغة الـerror نفسها.

استخرج:
framework/class names, module names, route names, internal hostnames, RPC methods, database terminology, build/version hints.

الـpivot:
error fingerprint → technology/framework → targeted endpoint/feature hypotheses.

مثال: error/debug information ظهر في تقارير bounty كـinformation disclosure؛ القيمة الحقيقية هي ما يمكنك اشتقاقه منه.

القاعدة: technology disclosure وحده ليس report؛ يجب أن ينتج attack-surface أو impact قابل للإثبات.

## Payload / Code

```
500
↓
exception/class
↓
framework/module
↓
targeted hypothesis
```

## Source

Intigriti information-disclosure guidance + disclosed HackerOne error/debug cases

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
