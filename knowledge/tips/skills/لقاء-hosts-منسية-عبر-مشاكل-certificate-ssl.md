# SKILL: لقاء Hosts منسية عبر مشاكل Certificate SSL

**Skill id:** `tip/لقاء-hosts-منسية-عبر-مشاكل-certificate-ssl`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081ea9ba4f4fb923b01d3  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

المطورين بينسوا يشيلوا hosts قديمة لو مش مهمة لهم. الـ hosts دي بتظهر shahadat SSL منتهية أو فيها مشاكل. راقبها واختبرها لأنها مش بتأخد نفس الاهتمام الأمني بتاع الأبلكيشن الرئيسي.

## Payload / Code

```
Shodan: ssl.cert.expired:true hostname:"[target.com](http://target.com)"
Censys: services.tls.certificates.leaf\_data.subject.common\_name:"[target.com](http://target.com)" and services.tls.certificates.leaf\_data.validity.end\<now
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 4)

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
