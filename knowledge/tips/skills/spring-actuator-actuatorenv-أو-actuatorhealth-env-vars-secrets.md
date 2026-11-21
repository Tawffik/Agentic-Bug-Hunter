# SKILL: Spring Actuator /actuator/env أو /actuator/health → env vars & secrets

**Skill id:** `tip/spring-actuator-actuatorenv-أو-actuatorhealth-env-vars-secrets`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ab822ffc40734a7f74  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في تطبيقات Spring Boot، الـ Actuator endpoints غالباً مكشوفة. /actuator/env بيرجع environment variables كاملة (DB passwords, API keys...). جرب كمان /actuator/mappings, /actuator/configprops, /actuator/heapdump.

## Payload / Code

```
[https://target.com/actuator/env](https://target.com/actuator/env)
[https://target.com/actuator/health](https://target.com/actuator/health)
[https://target.com/actuator/mappings](https://target.com/actuator/mappings)
```

## Source

Common high-value finding in Java/Spring apps (many bounties)

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
