# SKILL: Google API Key / Firebase Identity Toolkit — verify real auth impact, not key presence

**Skill id:** `tip/google-api-key-firebase-identity-toolkit-verify-real-auth-impact-not-key-presence`  
**Category:** Auth Bypass, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e880814491d0d85649ce22e8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A browser-visible Google API key is often an intended public identifier. Risk appears only if the associated Firebase/Identity Toolkit configuration or application authorization logic permits an unintended security-relevant action. A domain-based signup assumption is not proof of email ownership or authorization.

## Payload / Code

```
Review the app's documented signup flow and Firebase/Identity Toolkit configuration using only an owned test account and explicitly authorized scope. Check whether email verification is required where the product relies on it, and whether server-side access checks actually enforce the intended domain/role policy. Do not attempt access to other users' records or use exposed keys for unrelated services.
```

## Source

User-provided screenshot / Orwa-style research note; validation criteria normalized

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
