# SKILL: Forgotten QA / Staging subdomain → full document download without auth (\$800 case)

**Skill id:** `tip/forgotten-qa-staging-subdomain-full-document-download-without-auth-800-case`  
**Category:** Recon, IDOR  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808108a936f1ac6d08488e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, IDOR**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعد subdomain enum دور على qa. / staging. / test. / uat. / dev. حتى لو الـ main site محمي، الـ QA غالباً بيسيب documents (CSV/PDF) مفتوحة بدون login. في الحالة دي طلع proprietary trading data.

## Payload / Code

```
subfinder -d [target.com](http://target.com) \| httpx -title -status-code \| grep -iE 'qa\|staging\|test\|uat\|dev'
```

## Source

gopi krishnan Medium writeup – \$800 HackerOne (Feb 2026)

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
