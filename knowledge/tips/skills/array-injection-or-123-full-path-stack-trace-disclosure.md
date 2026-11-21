# SKILL: Array injection (\[\] or \[1,2,3\]) → Full Path / Stack Trace Disclosure

**Skill id:** `tip/array-injection-or-123-full-path-stack-trace-disclosure`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081bead23e5ffeda23d47  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

حط array في أي parameter (حتى لو مش متوقع). كتير من الـ frameworks بترمي error فيها full path أو stack trace أو internal class names. مفيد جدًا لـ path disclosure وخطأ oracle.

## Payload / Code

```
param\[\]=1
param\[1,2,3\]=test
param\[\]\[\]=1
```

## Source

Book of Bug Bounty Tips + multiple hunters

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
