# SKILL: Blind SSRF Detection عبر Interactsh

**Skill id:** `tip/blind-ssrf-detection-عبر-interactsh`  
**Category:** SSRF  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081e29fd9f35e211d645a  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الـ SSRF مش بترجع أي رد في الـ response (blind)، استخدم سيرفر out-of-band زي Interactsh للتأكد من وجود الثغرة عبر أي DNS/HTTP callback يوصلك.

## Payload / Code

```
1) تنصيب: go install -v [github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest](http://github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest)
2) تشغيل: interactsh-client -server [oast.pro](http://oast.pro) -n 5
3) حط الـ subdomain اللي طلعتلك مكان الـ URL المستهدف في الـ request
4) أي callback يرجع = تأكيد وجود الثغرة
```

## Source

Redfox Security 2026

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
