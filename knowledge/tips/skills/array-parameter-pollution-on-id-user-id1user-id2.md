# SKILL: Array / parameter pollution on ID (user\_id\[\]=1&user\_id\[\]=2)

**Skill id:** `tip/array-parameter-pollution-on-id-user-id1user-id2`  
**Category:** IDOR  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081988ac7df37a1f1fb31  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الـ backends بياخدوا أول أو آخر قيمة، أو بيعملوا array. جرب \[\] أو تكرار الباراميتر.

## Payload / Code

```
user\_id\[\]=victim&user\_id\[\]=attacker
id=1&id=2
```

## Source

Classic still works

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
