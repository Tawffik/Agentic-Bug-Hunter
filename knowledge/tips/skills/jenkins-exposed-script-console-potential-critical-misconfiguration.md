# SKILL: Jenkins exposed script console → potential critical misconfiguration

**Skill id:** `tip/jenkins-exposed-script-console-potential-critical-misconfiguration`  
**Category:** Recon, RCE  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081128cebf10a66f219e4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

وجود Jenkins أو مسار /script لا يثبت أن الـ console متاح دون مصادقة. تحقق من الاستجابة ومتطلبات تسجيل الدخول فقط. لا تنفذ Groovy أو أوامر على الخادم؛ صنّفها كخطر محتمل حتى يتوفر دليل آمن ومصرح به على تجاوز المصادقة.

## Payload / Code

```
curl [https://jenkins.target.com/script](https://jenkins.target.com/script)
# أو /api/json للتحقق
```

## Source

[BugBounty.info](http://BugBounty.info) playbook + multiple H1 reports

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
