# SKILL: Redis port 6379 exposed without auth

**Skill id:** `tip/redis-port-6379-exposed-without-auth`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880814d9d16e3ba3eda7bae  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

امسح 6379. لو مفتوح بدون requirepass، استخدم redis-cli عشان تقرأ keys أو تعمل CONFIG SET dir /var/www وتكتب shell.

## Payload / Code

```
redis-cli -h target-ip
KEYS \*
CONFIG GET \*
```

## Source

Common high-impact misconfig

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
