# SKILL: config.php / [settings.py](http://settings.py) / [application.properties](http://application.properties) / appsettings.json exposed

**Skill id:** `tip/configphp-settingspyhttpsettingspy-applicationpropertieshttpapplicationproperties-appsettingsjson-exposed`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808139879bc7ab99e30ef5  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ملفات الكونفيج دي غالبًا فيها DB credentials أو API keys. جرب الأسماء الشائعة + .bak/.old.

## Payload / Code

```
config.php, [settings.py](http://settings.py), [application.properties](http://application.properties), appsettings.json, database.php, conn.php
```

## Source

Common config file leaks

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
