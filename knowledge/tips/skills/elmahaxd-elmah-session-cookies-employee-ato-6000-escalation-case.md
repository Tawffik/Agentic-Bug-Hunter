# SKILL: Elmah.axd /elmah → Session cookies → Employee ATO (\$6,000 escalation case)

**Skill id:** `tip/elmahaxd-elmah-session-cookies-employee-ato-6000-escalation-case`  
**Category:** Recon, Auth Bypass  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808137ab29c8ed62e35bc6  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ضيف /elmah و /elmah.axd للكلمة. لو مفتوح، ادخل Details على أي log → هتلاقي full HTTP request بما فيها session cookies. خد الكوكي وجربه على الـ main site → غالباً employee أو admin ATO. لو الـ logs فاضية، راقبها ساعات لأن ساعات بتمسح hourly.

## Payload / Code

```
[https://target.com/elmah.axd](https://target.com/elmah.axd)
[https://target.com/elmah](https://target.com/elmah)
```

## Source

Jayesh Madnani tip – \$6000 from escalating Elmah disclosure

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
