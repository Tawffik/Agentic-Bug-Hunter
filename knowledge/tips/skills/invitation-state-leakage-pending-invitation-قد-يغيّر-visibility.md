# SKILL: ✉️ Invitation-State Leakage — pending invitation قد يغيّر Visibility

**Skill id:** `tip/invitation-state-leakage-pending-invitation-قد-يغيّر-visibility`  
**Category:** API Hacking, IDOR, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081ef949de9d64ac2ebfc  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, IDOR, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: وجود invitation/pending membership أحيانًا يجعل metadata أو resources تظهر قبل اكتمال authorization.

states:
invited / pending / accepted / expired / revoked.

ابحث عن: invitation IDs, membership endpoints, preview pages, email-link APIs, resource summaries.

مثال حقيقي: HackerOne disclosed report عن إمكانية رؤية titles لprivate reports مع pending email invitation وكان bounty كبيرًا.

الهدف: اكتشاف state/authorization mismatch، وليس محاولة قبول دعوات أو تغيير membership بشكل آلي.

## Payload / Code

```
invited
pending
accepted
expired
revoked
```

## Source

HackerOne disclosed bounty report — private report titles via pending invitation

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
