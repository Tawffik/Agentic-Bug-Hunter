# SKILL: Excessive API fields + GDPR/CCPA framing لرفع الـ Severity

**Skill id:** `tip/excessive-api-fields-gdprccpa-framing-لرفع-الـ-severity`  
**Category:** API Hacking, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880817dabcbd6d533b22ff4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لما الـ API بيرجع fields زيادة (address, phone, SSN last4, internal notes)، اكتب التقرير مع ذكر GDPR/CCPA risk و business impact (identity theft, regulatory fines). ده بيرفع الـ severity من Low/Medium لـ High في كتير من البرامج.

## Payload / Code

```
قارن الـ UI fields مع الـ raw JSON response
```

## Source

ToxSec Medium + Intigriti privacy guidance

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
