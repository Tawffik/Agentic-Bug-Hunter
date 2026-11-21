# SKILL: NFS shares misconfigured (showmount -e) → mount and read files

**Skill id:** `tip/nfs-shares-misconfigured-showmount-e-mount-and-read-files`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081cb8cd2f3a6f0184d69  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

امسح port 111/2049، بعدين showmount -e IP. لو فيه exports بدون restriction، mount واقرأ الملفات (configs، home dirs...).

## Payload / Code

```
showmount -e target-ip
mkdir /tmp/nfs && mount -t nfs target-ip:/export /tmp/nfs
```

## Source

Undercode Testing – common misconfig for bounties

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
