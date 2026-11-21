# SKILL: Internal browser extensions publicly accessible → hardcoded secrets

**Skill id:** `tip/internal-browser-extensions-publicly-accessible-hardcoded-secrets`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880810ab503fa285bb31aca  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الشركات بتعمل browser extensions داخلية للشغل، وأحيانًا بتنشرها بالغلط. Google dork أو enumeration بيلاقيها وفيها API keys و internal paths.

## Payload / Code

```
site:[chrome.google.com/webstore](http://chrome.google.com/webstore) "company name" OR site:[addons.mozilla.org](http://addons.mozilla.org) "company"
```

## Source

Intigriti 31 Tips 2026 (Tip about internal web extensions)

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
