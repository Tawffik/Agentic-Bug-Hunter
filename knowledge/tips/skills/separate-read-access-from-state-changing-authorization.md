# SKILL: Separate read access from state-changing authorization

**Skill id:** `tip/separate-read-access-from-state-changing-authorization`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e88081fa9a8dd34acec3ebf8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Authorization that permits reading an object does not imply permission to mutate it. Test GET/PUT/PATCH/POST/DELETE or GraphQL mutations separately and verify the state change from an independent view.

## Payload / Code

```
Use two accounts you own and a harmless test object in a lab. Change one non-sensitive field, then verify from the second account or an independent audit/log view.
```

## Source

[https://portswigger.net/web-security/access-control/idor](https://portswigger.net/web-security/access-control/idor)

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
