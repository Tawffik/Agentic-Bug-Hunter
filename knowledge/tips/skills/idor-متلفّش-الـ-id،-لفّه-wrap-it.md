# SKILL: IDOR: متلفّش الـ ID، لفّه (wrap it)

**Skill id:** `tip/idor-متلفّش-الـ-id،-لفّه-wrap-it`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e880813aba8ae587cb171c36  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ auth بيتحقق من المفتاح الخارجي (Outer key)، لكن الـ business logic بينفّذ على المفتاح الداخلي (Inner key). الـ scanners الأوتوماتيك بتفوّت النوع ده من IDOR لأنها مش بتلف الـ values.

## Payload / Code

```
❌ \{"Account": 1111\}
✅ \{"Account": \{"Account": 3333\}\}
```

## Source

vulnX @vuln\_X — #BugBounty #IDOR #APIHacking

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
