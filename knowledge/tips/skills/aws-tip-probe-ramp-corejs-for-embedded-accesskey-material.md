# SKILL: AWS tip: probe /ramp\_core.js for embedded AccessKey material

**Skill id:** `tip/aws-tip-probe-ramp-corejs-for-embedded-accesskey-material`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880815f9914f32ae7e5aca5  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض تطبيقات/SDK قديمة أو حزم front-end تضع مسارات ثابتة فيها مفاتيح أو config. إضافة /ramp\_core.js (ومسارات مشابهة من wordlists السحابية) لمرحلة content discovery قد تكشف AccessKeyId/Secret في JS. المفتاح وحده يحتاج إثبات صلاحية وتأثير داخل النطاق قبل البلاغ.

## Payload / Code

```
Add to content wordlist:
/ramp\_core.js
/.aws/credentials
/config.json
/aws-config.js
After hit: extract AKIA… patterns; verify only with program-allowed checks; never use keys outside authorized testing.
```

## Source

Mr\_mars\_hacker AWS tip (X)

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
