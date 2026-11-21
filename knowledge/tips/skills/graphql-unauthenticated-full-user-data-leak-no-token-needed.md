# SKILL: GraphQL unauthenticated → full user data leak (no token needed)

**Skill id:** `tip/graphql-unauthenticated-full-user-data-leak-no-token-needed`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808145b15ce4eb816f3294  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

دور على /graphql أو /api/graphql. جرب query بسيط بدون أي token. لو رجع user data (IDs, names, emails) → High impact. حتى لو introspection مقفول، جرب queries من الـ JS.

## Payload / Code

```
POST /graphql
\{"query":"\{ users \{ id username name email createdAt \} \}"\}
```

## Source

Omar Tamer Medium writeup 2026

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
