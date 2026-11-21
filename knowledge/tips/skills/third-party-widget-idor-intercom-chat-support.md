# SKILL: Third-party widget IDOR (Intercom / chat / support)

**Skill id:** `tip/third-party-widget-idor-intercom-chat-support`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e8808169ae1df7c335b27b74  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ chat/support widgets أحيانًا فيها user\_id أو conversation\_id unprotected. جرب تغير الـ ID.

## Payload / Code

```
Intercept widget API → change user/conversation ID
```

## Source

Real writeups 2026

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
