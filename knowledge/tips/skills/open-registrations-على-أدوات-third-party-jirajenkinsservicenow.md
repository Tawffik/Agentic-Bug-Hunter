# SKILL: Open Registrations على أدوات Third-Party (Jira/Jenkins/ServiceNow)

**Skill id:** `tip/open-registrations-على-أدوات-third-party-jirajenkinsservicenow`  
**Category:** Auth Bypass, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808111a3a2e53034967b3c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير الشركات بتنزّل منصات زي Jira وJenkins وServiceNow للاستخدام الداخلي لكن بتنسى تقفل الـ registrations العامة. لو لقيت الـ signup فاتح، هتقدر تعمل لك حساب وتشوف functionality داخلية موجودة للموظفين بس.

## Payload / Code

```
[target.com/jira/signup](http://target.com/jira/signup)
[target.com/servicenow/register](http://target.com/servicenow/register)
[target.com/jenkins/signup](http://target.com/jenkins/signup)
(جرّب أكتر من صيغة path لكل أداة)
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 9)

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
