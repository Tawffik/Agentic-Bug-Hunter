# SKILL: Password Reset token not bound to user / reusable

**Skill id:** `tip/password-reset-token-not-bound-to-user-reusable`  
**Category:** Password Reset  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081c0b610c1f7f991c481  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو التوكن شغال لأي يوزر أو مش مربوط بالـ email/user\_id → استخدمه على حساب تاني.

## Payload / Code

```
Request token for yourself → try on victim account endpoint
```

## Source

Classic high-impact

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
