# SKILL: 🌐 Historical Infrastructure Pivot — Historical Host/DNS/IP → Current Asset

**Skill id:** `tip/historical-infrastructure-pivot-historical-hostdnsip-current-asset`  
**Category:** Recon, Subdomain Enum  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081639ec7d0dea298d253  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: الـhistorical asset قد يقودك إلى infrastructure ما زال مرتبطًا بالهدف لكن اسمه الحالي مختلف.

pivot:
historical hostname → historical DNS/IP → related current hostnames → DNS/HTTP validation → scope.

مثال ذهني:
[old-api.example.com](http://old-api.example.com) → old IP → [current-api.example.com](http://current-api.example.com)

Evidence المطلوب: historical source + DNS relation + current resolution/HTTP evidence. لا تعتمد على IP وحده لإثبات ownership.

## Payload / Code

```
historical hostname
→ historical DNS/IP
→ current DNS
→ current related asset
```

## Source

Passive DNS / historical infrastructure research + bug bounty recon methodology

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
