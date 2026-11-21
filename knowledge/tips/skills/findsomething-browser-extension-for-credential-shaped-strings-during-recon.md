# SKILL: FindSomething browser extension for credential-shaped strings during recon

**Skill id:** `tip/findsomething-browser-extension-for-credential-shaped-strings-during-recon`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081d9ac06e1b3531e3f85  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

While browsing the target, FindSomething highlights potential secrets and interesting strings in page source and loaded assets. Useful as a passive assist next to JS Miner / manual review; always validate false positives.

## Payload / Code

```
Install FindSomething (browser extension)
Browse in-scope app pages and JS-heavy flows
Review highlighted candidates → classify public vs sensitive
Do not auto-report client-side publishable keys without impact
```

## Source

Mohamed Ahmed — FindSomething tip

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
