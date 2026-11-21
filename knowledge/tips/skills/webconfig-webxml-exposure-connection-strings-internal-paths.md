# SKILL: web.config / web.xml exposure → connection strings & internal paths

**Skill id:** `tip/webconfig-webxml-exposure-connection-strings-internal-paths`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808144b2a5d2dbb8389c44  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في IIS أو Tomcat، لو web.config أو web.xml مكشوفين، غالباً بيحتووا connection strings، machine keys، أو internal paths. جرب كمان /WEB-INF/web.xml.

## Payload / Code

```
[https://target.com/web.config](https://target.com/web.config)
[https://target.com/WEB-INF/web.xml](https://target.com/WEB-INF/web.xml)
```

## Source

Classic [ASP.NET](http://ASP.NET) / Java misconfig

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
