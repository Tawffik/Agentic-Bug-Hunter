# SKILL: UUID leak in invites / shared links / emails → IDOR

**Skill id:** `tip/uuid-leak-in-invites-shared-links-emails-idor`  
**Category:** IDOR, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880819eb8efe66969246ce2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

UUIDs مش حماية. دور عليها في invites, share links, emails, exports، بعدين استخدمها في endpoints تانية.

## Payload / Code

```
Find UUID in invite email → replay in /api/document/\{uuid\}
```

## Source

XSS Rat + top hunters

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
