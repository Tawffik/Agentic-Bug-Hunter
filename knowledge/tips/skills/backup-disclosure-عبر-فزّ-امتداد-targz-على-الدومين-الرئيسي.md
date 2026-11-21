# SKILL: Backup Disclosure عبر فزّ امتداد tar.gz على الدومين الرئيسي

**Skill id:** `tip/backup-disclosure-عبر-فزّ-امتداد-targz-على-الدومين-الرئيسي`  
**Category:** Recon, General  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3ffdac31e88081f28439f0efebdddbe6  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

فزّ الدومين الرئيسي (مش subdomain فرعي) بامتداد أرشيف شائع زي tar.gz بدل الوقوف عند .env أو .git بس. نسخة احتياطية كاملة لإعدادات التطبيق ممكن تتسرب فيها بيانات اعتماد قاعدة البيانات ومفاتيح المصادقة والأسرار كاملة. الدرس: نفس فكرة ملفات الباك اب المنسية (.env, .git, .svn/wc.db) بس بامتداد مختلف وعلى نطاق أساسي بدل فرعي.

## Payload / Code

```
fuzz: [main-domain.com/FUZZ](http://main-domain.com/FUZZ) with extension .tar.gz
(جرّب كمان .zip .rar .bak .old على نفس الدومين الرئيسي)
```

## Source

Kanhaiya Sharma (@krishnsec) — Standoff Bug Bounty, 12 Oct 2025, بونتي موثّق (8,081 views)

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
