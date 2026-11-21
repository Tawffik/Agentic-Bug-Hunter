# SKILL: Business Logic: race on wallet / coupon / referral

**Skill id:** `tip/business-logic-race-on-wallet-coupon-referral`  
**Category:** General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081cdb4d7e6f9e12cdddd  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

race condition على discount, referral credit, wallet top-up, أو one-time coupon. Turbo Intruder.

## Payload / Code

```
Send many parallel requests on apply-coupon / claim-referral
```

## Source

Top bugs 2026 + real cases

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
