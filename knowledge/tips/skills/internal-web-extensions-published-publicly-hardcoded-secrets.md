# SKILL: Internal web extensions published publicly → hardcoded secrets

**Skill id:** `tip/internal-web-extensions-published-publicly-hardcoded-secrets`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880818d9409ff18ba64669c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الشركات بتنشر internal Chrome/Firefox extensions بالغلط على الـ public stores. دور باسم الشركة + “extension” أو “plugin” في Chrome Web Store / Mozilla Add-ons. غالباً فيها API keys و internal endpoints.

## Payload / Code

```
site:[chrome.google.com/webstore](http://chrome.google.com/webstore) "company name"
site:[addons.mozilla.org](http://addons.mozilla.org) "company name"
```

## Source

Intigriti Bug Bytes #229 + previous tip enhancement

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
