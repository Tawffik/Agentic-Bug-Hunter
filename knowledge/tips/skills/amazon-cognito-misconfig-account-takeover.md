# SKILL: Amazon Cognito misconfig → Account Takeover

**Skill id:** `tip/amazon-cognito-misconfig-account-takeover`  
**Category:** Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081189531f2bae0f89119  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الـ User Pool misconfigured (مثلاً allow unauthenticated or weak identity pool)، تقدر تعمل ATO أو escalate privileges.

## Payload / Code

```
دور على Cognito User Pool ID في الـ JS / config
```

## Source

Intigriti archived writeup (iknowhatodo)

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
