# SKILL: Last-step authorization check in multi-step flows

**Skill id:** `tip/last-step-authorization-check-in-multi-step-flows`  
**Category:** IDOR, Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/403dac31e880813b8c76eec2ab764f6a  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو flow فيه preview ثم confirm أو create ثم commit، ما تفترضش إن check اللي حصل في أول خطوة اتنقل للخطوة الأخيرة. راقب آخر request مباشرة واختبره بحساب أقل صلاحية داخل لاب أو برنامج مصرح.

## Payload / Code

```
Compare the final commit request under the intended role and a lower-privileged test role. Stop at authorization proof; don't mutate real third-party data.
```

## Source

[https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls](https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls)

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
