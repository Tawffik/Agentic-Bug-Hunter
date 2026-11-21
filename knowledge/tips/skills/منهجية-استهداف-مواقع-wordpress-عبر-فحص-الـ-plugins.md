# SKILL: منهجية استهداف مواقع WordPress عبر فحص الـ Plugins

**Skill id:** `tip/منهجية-استهداف-مواقع-wordpress-عبر-فحص-الـ-plugins`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081868410c20faeb172de  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أكتر من نص موقع بيشتغل WordPress. المنهجية: اكتشف الـ plugins المفعّلة من الـ source code، فزّينج plugins مخفية، ودور على الـ versions القديمة معروف فيها ثغرات في WPScan database.

## Payload / Code

```
1) اكتشف scripts/style sheets مدزودة بـ wp-content/plugins/
2) فزّينج: ffuf -u [target.com/wp-content/plugins/FUZZ](http://target.com/wp-content/plugins/FUZZ) -w plugin-list.txt
3) افحص رقم الإصدار مقابل CVE في WPScan Vulnerability Database
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 23)

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
