# SKILL: GitHub Dork: CI/CD dangerous patterns

**Skill id:** `tip/github-dork-cicd-dangerous-patterns`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880810ab323dd4e179eaf11  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

pull\_request\_target + secrets: inherit = classic supply-chain risk.

## Payload / Code

```
org:TARGET path:.github/workflows ("pull\_request\_target" OR "secrets: inherit" OR "permissions: write-all")
```

## Source

Your own Dorks page + Intigriti

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
