# SKILL: WordPress /\_wpeprivate/config.json Information Disclosure

**Skill id:** `tip/wordpress-wpeprivateconfigjson-information-disclosure`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081399147fb4dd7b446fe  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

على مواقع WordPress (خصوصًا WP Engine)، جرب المسار /\_wpeprivate/config.json. غالبًا بيرجع معلومات حساسة عن الـ configuration.

## Payload / Code

```
[https://target.com/\_wpeprivate/config.json](https://target.com/_wpeprivate/config.json)
```

## Source

Anton @therceman tip (high engagement)

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
