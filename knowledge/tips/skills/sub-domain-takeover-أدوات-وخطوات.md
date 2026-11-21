# SKILL: Sub Domain Takeover — أدوات وخطوات

**Skill id:** `tip/sub-domain-takeover-أدوات-وخطوات`  
**Category:** Subdomain Enum  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e880813a92cec156d363a76b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

جمع الساب دومينز من مصادر متعددة (findomain + reverse whois)، دمجهم، فلترتهم عن طريق httpx للتأكد من إنهم شغالة، تمهيدًا للبحث عن CNAME records بتشاور على خدمة اتلغت (subdomain takeover).

## Payload / Code

```
hunt subdomains: findomain -r لجمع الساب دومينز
hunt acquisitions: reverse whois محفوظة في combined subs.txt
combinedsubs.txt \| sort -u \| httpx \| tee finalsubs.txt
```

## Source

Rohin Jain @th3ho... — Bug Bounty Tip #7

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
