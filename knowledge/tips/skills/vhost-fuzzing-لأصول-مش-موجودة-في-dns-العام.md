# SKILL: Vhost Fuzzing لأصول مش موجودة في DNS العام

**Skill id:** `tip/vhost-fuzzing-لأصول-مش-موجودة-في-dns-العام`  
**Category:** Recon, Subdomain Enum  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808182ba31e5a8f1216a82  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير من الأصول مش مدرجة في الـ public DNS بس لسه شغالة لو حطيت الـ Host header الصح. استخدم ffuf مع قائمة subdomains ضد الـ IP الحقيقي.

## Payload / Code

```
ffuf -w subdomains.txt -u [https://TARGET\_IP](https://TARGET_IP) -H "Host: [FUZZ.target.com](http://FUZZ.target.com)" -fs 0
```

## Source

Intigriti 31 Tips 2026

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
