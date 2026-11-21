# SKILL: Google Alerts on your dorks — monitor new indexed exposure

**Skill id:** `tip/google-alerts-on-your-dorks-monitor-new-indexed-exposure`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880816b8ed9fc12091a13e9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Turn high-value Google dorks into Google Alerts so newly indexed pages matching the query are emailed. Good for long-running programs where content appears after deploys or misconfigurations.

## Payload / Code

```
1) Craft dork (e.g. site:[target.com](http://target.com) ext:env)
2) Google Alerts → create alert for that query
3) Frequency: as-it-happens or daily
4) Triage each hit for scope + sensitivity

Tip list reference often shared with dork monitoring blogs (SecurityTrails-style guides).
```

## Source

Wesley Luna — Google Alerts for dorks

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
