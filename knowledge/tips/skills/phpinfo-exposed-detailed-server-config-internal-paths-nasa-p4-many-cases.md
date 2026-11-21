# SKILL: phpinfo() exposed → detailed server config + internal paths (NASA P4 + many cases)

**Skill id:** `tip/phpinfo-exposed-detailed-server-config-internal-paths-nasa-p4-many-cases`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808121ba9ed039d9d8d672  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

دور على phpinfo.php / info.php / test.php / phpinfo. بيرجع PHP version، internal paths، loaded modules، environment variables، وأحيانًا internal IPs. مفيد للـ chaining مع LFI أو RCE.

## Payload / Code

```
ffuf -u [https://target.com/FUZZ](https://target.com/FUZZ) -w phpinfo\_wordlist.txt -mc 200
# common: phpinfo.php, info.php, test.php, i.php
```

## Source

MattKingst NASA VDP (P4 resolved) + common bounty findings

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
