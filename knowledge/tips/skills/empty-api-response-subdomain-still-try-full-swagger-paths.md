# SKILL: Empty API response subdomain → still try full Swagger paths

**Skill id:** `tip/empty-api-response-subdomain-still-try-full-swagger-paths`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808107ae85c81acf415708  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

حتى لو الـ API subdomain بيرجع empty body، جرب المسارات الكاملة لـ Swagger: /swagger-ui.html /swagger/index.html /api/swagger-ui.html /v1/swagger-ui.html /swagger/swagger-ui.html

## Payload / Code

```
ffuf -u [https://api.target.com/FUZZ](https://api.target.com/FUZZ) -w swagger\_paths.txt -mc 200
```

## Source

Book of BugBounty Tips

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
