# SKILL: phpMyAdmin / adminer.php unauthenticated (auth\_type=config)

**Skill id:** `tip/phpmyadmin-adminerphp-unauthenticated-auth-typeconfig`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808157a10ffc552944c63a  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

دور على /phpmyadmin أو /adminer.php أو /admin/adminer.php. لو auth\_type=config ومفتوح، تقدر تقرأ/تكتب الـ DB كامل بما فيها hashes.

## Payload / Code

```
[https://target.com/phpmyadmin/](https://target.com/phpmyadmin/)
[https://target.com/adminer.php](https://target.com/adminer.php)
```

## Source

GitHub advisory + common misconfig

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
