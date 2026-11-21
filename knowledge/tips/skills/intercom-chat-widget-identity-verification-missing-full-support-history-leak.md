# SKILL: Intercom chat widget identity verification missing → full support history leak

**Skill id:** `tip/intercom-chat-widget-identity-verification-missing-full-support-history-leak`  
**Category:** API Hacking, IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880815582fcd5ac07474859  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير شركات بتستخدم Intercom بدون identity verification. تقدر impersonate أي user وتقرأ كل الـ support chat history (PII + internal notes).

## Payload / Code

```
دور على intercom settings في الـ JS، جرب تغير user\_id / email بدون verification token
```

## Source

Intigriti Bug Bytes #229 (Oct 2025) – multiple critical cases

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
