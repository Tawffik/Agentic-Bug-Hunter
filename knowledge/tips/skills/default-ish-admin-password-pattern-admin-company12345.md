# SKILL: Default-ish admin password pattern: admin / \[company\]12345

**Skill id:** `tip/default-ish-admin-password-pattern-admin-company12345`  
**Category:** Auth Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808107b2c0eb20e665051d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Some internal or legacy admin panels still use predictable defaults built from the company name. Only test on in-scope login surfaces with program-allowed credentials testing; never spray broadly.

## Payload / Code

```
Username: admin
Password candidates (examples only):
\[company\]12345
\[company\]1234
\[Company\]@123
admin@\[company\]

Prefer single-target manual checks over mass spraying. Log only whether login succeeded for your test account scope.
```

## Source

Mohamed Ahmed — default password tip

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
