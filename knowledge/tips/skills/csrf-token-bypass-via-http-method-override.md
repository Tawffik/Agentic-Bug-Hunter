# SKILL: CSRF token bypass via HTTP method override

**Skill id:** `tip/csrf-token-bypass-via-http-method-override`  
**Category:** CSRF, Auth Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808166971be1b5e0135e8f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **CSRF, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Some apps only enforce CSRF tokens on POST. Switching method to GET with X-HTTP-Method-Override: POST, or using PUT/DELETE, can skip the token check while the backend still performs the state change. Confirm SameSite and cookie behavior; only test authorized actions on your accounts.

## Payload / Code

```
Original: POST /change-email with CSRF token
Test: GET /[change-email?email=attacker@x.com](mailto:change-email?email=attacker@x.com)
Header: X-HTTP-Method-Override: POST
Also try: X-HTTP-Method: PUT , \_method=POST form field
```

## Source

Twitter/X @yogsec — CSRF Token Bypass via Method Override (Nov 2026)

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
