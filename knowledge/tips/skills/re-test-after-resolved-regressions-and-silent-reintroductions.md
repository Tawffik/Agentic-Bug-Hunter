# SKILL: Re-test after "Resolved" — regressions and silent reintroductions

**Skill id:** `tip/re-test-after-resolved-regressions-and-silent-reintroductions`  
**Category:** General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808140a3d7c221fc28e6a0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعد إغلاق تقرير، الفرق أحيانًا تعيد كودًا قديمًا أو تصلّح مسارًا وتترك bypass. أعد نفس الـPoC بعد أسابيع على نفس النطاق المصرّح؛ لو عاد الخلل فهو تقرير regression جديد بأدلة حديثة.

## Payload / Code

```
Keep a private checklist of resolved PoCs per program.
Re-run exact steps + one common bypass variant after patch notes or 30–60 days.
```

## Source

Haythem tip (X)

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
