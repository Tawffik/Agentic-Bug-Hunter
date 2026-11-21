# SKILL: Hidden Parameter Discovery بأداة Arjun

**Skill id:** `tip/hidden-parameter-discovery-بأداة-arjun`  
**Category:** API Hacking, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808145bcc2d7bf51e33ab1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أداة Arjun بتدور على باراميترات مخفية في أي endpoint (مش موثقة). الباراميترات دي غالبًا بتفتح debug modes أو admin flags أو features مش موثقة.

## Payload / Code

```
arjun -u [https://api.target.com/v1/user/profile](https://api.target.com/v1/user/profile) --headers "Authorization: Bearer \" -m POST --stable -oJ output.json
```

## Source

Redfox Security 2026

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
