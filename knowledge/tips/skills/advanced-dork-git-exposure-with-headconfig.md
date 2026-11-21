# SKILL: Advanced Dork: .git exposure with HEAD/config

**Skill id:** `tip/advanced-dork-git-exposure-with-headconfig`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081008d8ee4888a0e4ac2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ده dork لاكتشاف صفحات قد تشير إلى كشف .git، لكنه يعتمد على فهرسة محركات البحث وقد يرجع نتائج قديمة أو نتائج غير مؤكدة. افتح النتيجة يدويًا داخل نطاق البرنامج، وتحقق من إمكانية قراءة ملف غير حساس مثل HEAD. لا تعتبر مجرد ظهور المسار إثباتًا لكشف المستودع.

## Payload / Code

```
site:[target.com](http://target.com) inurl:.git ("HEAD" OR "config" OR "index of")
```

## Source

[dorksearch.com](http://dorksearch.com) + Proviesec + real cases

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
