# SKILL: Backup tar.gz / .zip / .sql على الـ root domain مباشرة

**Skill id:** `tip/backup-targz-zip-sql-على-الـ-root-domain-مباشرة`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880818a918adeabf4d5f6e1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مش بس على subdomains. جرب الامتدادات الشائعة على الدومين الرئيسي نفسه: /backup.tar.gz, /db.sql, /[site.zip](http://site.zip), /[backup.zip](http://backup.zip), /.env.bak. كتير من الـ misconfigs بتحصل على الـ root.

## Payload / Code

```
ffuf -w backups.txt -u [https://target.com/FUZZ](https://target.com/FUZZ) -e .tar.gz,.zip,.sql,.bak,.old
```

## Source

Multiple real bounties + Kanhaiya Sharma style writeups

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
