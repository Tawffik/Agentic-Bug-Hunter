# SKILL: Directory listing enabled (especially /wp-content, /uploads, /backup)

**Skill id:** `tip/directory-listing-enabled-especially-wp-content-uploads-backup`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880810b9e00f56d506a7c6b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لما directory listing مفتوح، تقدر تشوف كل الملفات. ركز على /wp-content/uploads, /backup, /old, /temp.

## Payload / Code

```
[https://target.com/wp-content/](https://target.com/wp-content/)
[https://target.com/uploads/](https://target.com/uploads/)
```

## Source

Intigriti WordPress guide

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
