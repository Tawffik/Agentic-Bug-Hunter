# SKILL: Bypass الدفع بالـ Test Cards المنسية في Production

**Skill id:** `tip/bypass-الدفع-بالـ-test-cards-المنسية-في-production`  
**Category:** General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880811282eed806f1575cac  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض المطورين بينسوا يشيلوا test cards بتاعة payment gateways (Stripe, PayPal) في الـ Production. لو اشتغلت، ممكن تعمل orders بدون ما تتخصم فلوس.

## Payload / Code

```
jarrib cards معروفة زي: 4242 4242 4242 4242 (Stripe test card) على الـ production checkout
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 22)

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
