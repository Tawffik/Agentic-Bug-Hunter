# SKILL: package-lock.json / yarn.lock / composer.lock → dependency versions + potential vulns

**Skill id:** `tip/package-lockjson-yarnlock-composerlock-dependency-versions-potential-vulns`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808165bf4ace772a2d4da2  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الملفات دي بتتكشف أحيانًا. بتكشف exact dependency versions → تقدر تدور على CVEs معروفة في المكتبات دي وترفع الـ impact.

## Payload / Code

```
[https://target.com/package-lock.json](https://target.com/package-lock.json)
[https://target.com/yarn.lock](https://target.com/yarn.lock)
[https://target.com/composer.lock](https://target.com/composer.lock)
```

## Source

Modern recon practice (helps with known CVE chaining)

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
