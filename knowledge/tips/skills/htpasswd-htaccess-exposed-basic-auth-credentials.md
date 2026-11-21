# SKILL: .htpasswd / .htaccess exposed → Basic Auth credentials

**Skill id:** `tip/htpasswd-htaccess-exposed-basic-auth-credentials`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808121a662e6948b25b87e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو .htpasswd مكشوف، تقدر تعمل crack للـ hashes وتدخل على الـ protected areas.

## Payload / Code

```
[https://target.com/.htpasswd](https://target.com/.htpasswd)
[https://target.com/.htaccess](https://target.com/.htaccess)
```

## Source

Classic misconfig

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
