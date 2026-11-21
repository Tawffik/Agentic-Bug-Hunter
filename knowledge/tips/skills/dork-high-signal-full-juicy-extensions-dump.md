# SKILL: Dork (High Signal): Full juicy extensions dump

**Skill id:** `tip/dork-high-signal-full-juicy-extensions-dump`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880810b9877c1087160566e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أشهر دورك بيجيب ملفات حساسة مكشوفة. استخدمه مع site:[target.com](http://target.com).

## Payload / Code

```
site:[target.com](http://target.com) (ext:log OR ext:txt OR ext:conf OR ext:cnf OR ext:ini OR ext:env OR ext:sh OR ext:bak OR ext:backup OR ext:swp OR ext:old OR ext:\~ OR ext:git OR ext:svn OR ext:htpasswd OR ext:htaccess OR ext:json OR ext:yaml OR ext:yml OR ext:pem OR ext:key)
```

## Source

Proven lists (1BlackLine / reewardius / SecurityElites 2026)

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
