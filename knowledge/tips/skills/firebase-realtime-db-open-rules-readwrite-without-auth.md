# SKILL: Firebase Realtime DB open rules (read/write without auth)

**Skill id:** `tip/firebase-realtime-db-open-rules-readwrite-without-auth`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081008d0ae3d02b5db491  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

دور على [PROJECT.firebaseio.com](http://PROJECT.firebaseio.com) أو من الـ JS. جرب /.json بدون auth. لو رجع data أو قبل write → High.

## Payload / Code

```
curl [https://PROJECT-default-rtdb.firebaseio.com/.json](https://PROJECT-default-rtdb.firebaseio.com/.json)
curl -X PUT -d '\{"test":1\}' [https://PROJECT-default-rtdb.firebaseio.com/test.json](https://PROJECT-default-rtdb.firebaseio.com/test.json)
```

## Source

Multiple 2025-2026 writeups + GCP playbook

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
