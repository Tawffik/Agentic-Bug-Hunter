# SKILL: 🚩 Disabled Feature → Live API — الـUI يقول Disabled لكن الـBackend قد يظل يقبل الطلب

**Skill id:** `tip/disabled-feature-live-api-الـui-يقول-disabled-لكن-الـbackend-قد-يظل-يقبل-الطلب`  
**Category:** API Hacking, Auth Bypass, Recon  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e8808189bbfbecd930d2d100  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Auth Bypass, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: feature flag أو disabled UI لا يساوي enforcement على الـbackend.

اكتشف من JS/API:
disabled / deprecated / legacy / experimental / beta / feature flags.

ثم اربط flag بالـroute/method/object الذي يستخدمه.

Signal: feature disabled في client + endpoint ما زال reachable أو يعيد operation/data غير متوقعة.

لا تنفذ destructive state changes آليًا؛ اكتفِ بـsafe read/metadata validation حيث يسمح scope.

## Payload / Code

```
feature flag
   ↓
route/method
   ↓
backend reachability
   ↓
authorization/state check
```

## Source

HackerOne one-million-report dataset — disabled-agent/API behavior case

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
