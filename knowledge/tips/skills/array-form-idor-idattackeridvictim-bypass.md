# SKILL: Array-form IDOR — id\[\]=attacker&id\[\]=victim bypass

**Skill id:** `tip/array-form-idor-idattackeridvictim-bypass`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880810aa50ac331247d1c11  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ACL sometimes checks a single scalar id. Sending the same parameter as an array (id\[\]= or id as JSON array) can make the backend iterate and return or act on a second ID without ownership checks. Compare single-id 403 vs array 200 on authorized test objects only.

## Payload / Code

```
id=attacker\_id  → 403
id\[\]=attacker\_id&id\[\]=victim\_id  → 200?
id=\[attacker\_id, victim\_id\]  (JSON)
Also: ids=1,2 or objects\[0\]\[id\]=victim
```

## Source

Twitter/X IDOR edge-case tips (array/list parameters) + 2026 hunting notes

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
