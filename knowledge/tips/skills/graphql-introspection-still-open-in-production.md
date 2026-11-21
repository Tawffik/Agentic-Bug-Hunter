# SKILL: GraphQL introspection still open in production

**Skill id:** `tip/graphql-introspection-still-open-in-production`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880814e9f25faa619e8a622  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو introspection شغال، خد الـ full schema. ده بيسهل IDOR و BOLA و mutation abuse بشكل كبير.

## Payload / Code

```
\{\_\_schema\{queryType\{name\} mutationType\{name\} types\{name fields\{name\}\}\}\}
```

## Source

Common high-value finding + multiple writeups

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
