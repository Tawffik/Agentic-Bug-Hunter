# SKILL: Disable JavaScript → legacy / forgotten form still live

**Skill id:** `tip/disable-javascript-legacy-forgotten-form-still-live`  
**Category:** Recon, Auth Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880811ab193dc976204dc8c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

SPA frontends often hide or replace old flows with JS. Turning JS off (or fetching without executing scripts) can expose forgotten HTML forms and endpoints still wired on the server. Bots rarely do this. Use only on authorized targets; document the exact path and impact.

## Payload / Code

```
Browser: disable JS → reload sensitive flows (password reset, recovery, signup)
curl without following SPA redirects; compare HTML to JS-enabled view
Look for old form actions still posting to live APIs
```

## Source

Twitter/X @dd\_pwnd — Google account recovery with JS off loaded an old form that leaked phone numbers (\$5k, 2025 story retold 2026)

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
