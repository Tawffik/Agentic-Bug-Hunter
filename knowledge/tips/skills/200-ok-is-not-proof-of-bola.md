# SKILL: 200 OK is not proof of BOLA

**Skill id:** `tip/200-ok-is-not-proof-of-bola`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/403dac31e88081d0be18dd5b747ed4db  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـstatus code لوحده مش finding. لازم تثبت إن response رجّع object مختلف أو إن state اتغيّر فعلاً. قارن body/headers/length، وبعدها اعمل verification من مالك object في حساب تاني تملكه.

## Payload / Code

```
Use a harmless canary value in a lab and verify it from the second controlled account. Treat redirects, generic success JSON, and identical empty bodies as inconclusive.
```

## Source

[https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls](https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls)

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
