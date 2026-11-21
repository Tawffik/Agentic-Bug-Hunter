# SKILL: Apache server-status / server-info مكشوف → internal info + active requests

**Skill id:** `tip/apache-server-status-server-info-مكشوف-internal-info-active-requests`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880815c9598edfc24e6f15e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

/server-status بيرجع active connections، request URLs، client IPs. /server-info بيكشف modules و configuration. مفيد للـ recon العميق.

## Payload / Code

```
[https://target.com/server-status](https://target.com/server-status)
[https://target.com/server-info](https://target.com/server-info)
[https://target.com/server-status?auto](https://target.com/server-status?auto)
```

## Source

Common misconfig still found in 2025-2026

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
