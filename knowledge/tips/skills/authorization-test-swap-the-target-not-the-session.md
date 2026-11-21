# SKILL: Authorization test: swap the target, not the session

**Skill id:** `tip/authorization-test-swap-the-target-not-the-session`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/403dac31e880816f8138ea380dd994e7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في أي request authenticated، افصل بين هوية الـsession وبين object ID الموجود في الـpath/body. جرّب نفس session مع object تاني تملكه أنت. الهدف إثبات إن السيرفر بيربط القرار بالـsubject الصحيح، مش بمجرد إن المستخدم logged in.

## Payload / Code

```
Safe lab idea: Account A session + Account B test object ID. Change only a harmless field such as nickname. Confirm the change from Account B.
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
