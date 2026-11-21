# SKILL: Hardcoded third-party Analytics Write Key in JS → unauth data injection

**Skill id:** `tip/hardcoded-third-party-analytics-write-key-in-js-unauth-data-injection`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880817bbcddf32a95b46851  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في الـ login page أو main JS bundle دور على write\_key أو td\_write\_key أو similar لـ TreasureData / Segment / Mixpanel. لو write permission، تقدر تبعت fake events للـ production analytics بدون أي auth.

## Payload / Code

```
grep -Eo '(write\_key\|api\_key\|secret\|token)\["''\]?\\s\*\[:=\]\\s\*\["''\]\[a-zA-Z0-9/\_-\]+\["''\]' bundle.js
```

## Source

yash4078-ops GitHub writeup 2026 – Bounty Awarded (P3)

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
