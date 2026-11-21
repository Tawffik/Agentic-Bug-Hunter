# SKILL: Dork (High Signal): Test / Staging / Dev environments

**Skill id:** `tip/dork-high-signal-test-staging-dev-environments`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e8808169871ccdc6a8a2a693  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

البيئات دي غالباً أضعف حماية وبتجيب secrets أسهل.

## Payload / Code

```
site:[target.com](http://target.com) (inurl:test OR inurl:dev OR inurl:staging OR inurl:sandbox OR inurl:debug OR inurl:temp OR inurl:internal OR inurl:demo OR inurl:qa)
```

## Source

taksec + common bounty wins

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
