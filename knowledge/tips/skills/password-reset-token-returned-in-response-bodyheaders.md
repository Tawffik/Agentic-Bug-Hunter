# SKILL: Password Reset token returned in response body/headers

**Skill id:** `tip/password-reset-token-returned-in-response-bodyheaders`  
**Category:** Password Reset  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081509b4bc24a45158fbd  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الـ APIs بترجع التوكن في الـ response بدل ما تبعت إيميل فقط. لو كده → ATO مباشر.

## Payload / Code

```
POST /forgot-password \{"email":"victim"\}
→ Check response for token / link
```

## Source

Common still-found tip

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
