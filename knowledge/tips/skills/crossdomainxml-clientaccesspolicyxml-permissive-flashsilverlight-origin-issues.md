# SKILL: crossdomain.xml / clientaccesspolicy.xml permissive → Flash/Silverlight origin issues

**Skill id:** `tip/crossdomainxml-clientaccesspolicyxml-permissive-flashsilverlight-origin-issues`  
**Category:** Recon  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808115998ecbc9c59515e7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الملف بيسمح لأي domain (\*)، ممكن يستخدم في بعض الـ legacy attacks أو كـ info disclosure عن الـ allowed origins.

## Payload / Code

```
[https://target.com/crossdomain.xml](https://target.com/crossdomain.xml)
[https://target.com/clientaccesspolicy.xml](https://target.com/clientaccesspolicy.xml)
```

## Source

Older but still checked in some programs

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
