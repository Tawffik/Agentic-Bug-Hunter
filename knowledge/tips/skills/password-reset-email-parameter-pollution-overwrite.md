# SKILL: Password Reset email parameter pollution / overwrite

**Skill id:** `tip/password-reset-email-parameter-pollution-overwrite`  
**Category:** Password Reset  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880818695dfc481fa608765  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

جرب تغيّر الباراميتر بعد ما يتبعت، أو تضيف باراميتر تاني زي new\_email / redirect.

## Payload / Code

```
[email=victim@x.com](mailto:email=victim@x.com)&redirect=[https://attacker.com](https://attacker.com)
email=victim&new\_email=attacker
```

## Source

Checklist 2026

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
