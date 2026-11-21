# SKILL: Discover quieter bug bounty programs via Slack dork

**Skill id:** `tip/discover-quieter-bug-bounty-programs-via-slack-dork`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808178880fcddb8c1ef444  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Many companies publish security/bug bounty status on Slack directories or pages indexed by Google. A simple dork finds program mentions that are less crowded than top HackerOne lists.

## Payload / Code

```
site:[slack.com](http://slack.com) "Has a bug bounty program"
site:slack\[.\]com "Has a bug bounty program"

Then open official policy URL from the page (example pattern: responsible-disclosure pages).
```

## Source

AnmolSecSavvy — site:[slack.com](http://slack.com) Has a bug bounty program · Oct 2025

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
