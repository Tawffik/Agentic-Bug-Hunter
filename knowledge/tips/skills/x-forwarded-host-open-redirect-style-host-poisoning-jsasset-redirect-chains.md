# SKILL: X-Forwarded-Host open-redirect style host poisoning (JS/asset redirect chains)

**Skill id:** `tip/x-forwarded-host-open-redirect-style-host-poisoning-jsasset-redirect-chains`  
**Category:** Auth Bypass, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880811ca307eb40cb8a7b4c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بخلاف password-reset Host injection المعروف، بعض الـCDNs/الـapps تبني absolute URLs لملفات JS أو redirects من X-Forwarded-Host. جرّب تسلسل hostnames (target، [sub.target](http://sub.target)، nested) وراقب Location وContent-Location وروابط السكربت. الأثر القوي: تسميم سكربت يُحمَّل من أصل موثوق أو سرقة OAuth redirect.

## Payload / Code

```
X-Forwarded-Host: [target.com](http://target.com)
X-Forwarded-Host: [sub1.target.com](http://sub1.target.com)
X-Forwarded-Host: [sub2.sub1.target.com](http://sub2.sub1.target.com)
Also try: Forwarded: host=attacker.tld
Observe whether static/JS responses rewrite absolute URLs to attacker host.
```

## Source

dk4trin reply on X-Forwarded-Host bypass chain

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
