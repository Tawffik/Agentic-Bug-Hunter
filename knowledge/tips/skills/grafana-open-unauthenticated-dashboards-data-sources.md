# SKILL: Grafana open / unauthenticated → dashboards + data sources

**Skill id:** `tip/grafana-open-unauthenticated-dashboards-data-sources`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880811c92d9d605baafd78c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

دور على Grafana (port 3000 أو /grafana). لو مفيش login، تقدر تشوف dashboards، metrics، وأحيانًا data sources فيها secrets.

## Payload / Code

```
[https://target.com/grafana/](https://target.com/grafana/)
[https://target:3000/login](https://target:3000/login)
```

## Source

Common Shodan finding + recent CVEs

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
