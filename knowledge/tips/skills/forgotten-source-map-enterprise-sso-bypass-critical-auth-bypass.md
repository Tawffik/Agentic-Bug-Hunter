# SKILL: Forgotten Source Map → Enterprise SSO Bypass (Critical Auth Bypass)

**Skill id:** `tip/forgotten-source-map-enterprise-sso-bypass-critical-auth-bypass`  
**Category:** Recon, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081748c2ac5b8dfd98dd8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Source map كشف backend URLs + SignalR hub. اكتشف إن الـ client-side بيبعت x-ms-client-userid وهمي والـ backend بيصدقه → spoof أي user ID → bypass SSO كامل.

## Payload / Code

```
1. لاقي .map
2. فك الكود
3. دور على apiUrl / memberUrl / SignalR negotiate
4. جرب POST /negotiate مع header مزور
```

## Source

Priyansh writeup on InfoSec Write-ups (June 2026) – Critical finding

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
