# SKILL: Subdomain Permutations: خد الساب دومينز وولّد احتمالات جديدة

**Skill id:** `tip/subdomain-permutations-خد-الساب-دومينز-وولّد-احتمالات-جديدة`  
**Category:** Subdomain Enum, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081ab9075c54b54a4c876  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Subdomain Enum, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

معظم الناس بتوقف عند enum الساب دومينز بس. الخطوة الأقوى إنك تاخد الساب دومينز الموجودة وتولّد منها permutations (احتمالات تسمية) وتعمل resolve لكل احتمال، وده بيكشف بيئات dev/staging/backup منسية.

## Payload / Code

```
الفكرة: [dev.example.com](http://dev.example.com) → api/backup/backend/mail/demo/ftp/internal → [apidev.example.com](http://apidev.example.com), [api-dev.example.com](http://api-dev.example.com), [backupdev.example.com](http://backupdev.example.com)...الخ

أدوات:
- Altdns: [github.com/infosec-au/altdns](http://github.com/infosec-au/altdns)
- dnsgen: [github.com/AlephNullSK/dnsgen](http://github.com/AlephNullSK/dnsgen)
- gotator
```

## Source

obscaries \| AppSec

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
