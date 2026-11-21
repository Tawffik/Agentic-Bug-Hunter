# SKILL: GraphQL Introspection Schema Leak → \$5,500 Bounty

**Skill id:** `tip/graphql-introspection-schema-leak-5500-bounty`  
**Category:** API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081c79df2fd2ad54c45aa  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

حتى لو introspection مقفول في الـ main، جرب alternate endpoints أو \_\_schema query أو batching. في حالة حقيقية طلع الـ schema كامل وحدد كل الـ attack surface → \$5.5k.

## Payload / Code

```
query \{ \_\_schema \{ types \{ name fields \{ name \} \} \} \}
```

## Source

SecurityCipher daily writeups (Oct 2026) – \$5,500 reported

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
