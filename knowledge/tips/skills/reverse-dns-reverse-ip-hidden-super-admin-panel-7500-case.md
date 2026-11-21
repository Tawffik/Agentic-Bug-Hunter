# SKILL: Reverse DNS / Reverse IP → hidden Super Admin panel (\$7,500 case)

**Skill id:** `tip/reverse-dns-reverse-ip-hidden-super-admin-panel-7500-case`  
**Category:** Recon, Subdomain Enum  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081d4899ef3b6be8c8838  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مش بس subdomain enum. خد الـ IPs من الـ known assets واعمل reverse DNS / reverse IP lookup. غالباً بيطلع private subdomains مش ظاهرة في certificate transparency ولا public DNS → admin panels بدون auth.

## Payload / Code

```
for ip in $(cat ips.txt); do dig -x $ip +short; done
# أو استخدم tools زي hakrevdns / dnsx
```

## Source

Ahmed Ghadban Medium – \$7,500 Critical (Dec 2025)

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
