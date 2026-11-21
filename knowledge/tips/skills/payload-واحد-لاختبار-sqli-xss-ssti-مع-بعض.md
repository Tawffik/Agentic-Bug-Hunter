# SKILL: Payload واحد لاختبار SQLi + XSS + SSTI مع بعض

**Skill id:** `tip/payload-واحد-لاختبار-sqli-xss-ssti-مع-بعض`  
**Category:** SQLi, XSS, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081deaf9cf7f5ed2f335c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi, XSS, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ ' و " لاختبار SQL Injection، الـ \ لاختبار XSS، و \{\{1234\*6543\}\} لاختبار SSTI/CSTI (لو ظهر ناتج الضرب في الصفحة يبقى فيه SSTI).

## Payload / Code

```
'">\\{\{1234\*6543\}\}
```

## Source

rapiddns @rapid... — source: [medium.com/@vignesh4303](http://medium.com/@vignesh4303)

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
