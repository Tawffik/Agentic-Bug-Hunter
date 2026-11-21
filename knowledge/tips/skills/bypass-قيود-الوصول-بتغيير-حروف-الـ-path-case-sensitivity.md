# SKILL: Bypass قيود الوصول بتغيير حروف الـ Path (Case Sensitivity)

**Skill id:** `tip/bypass-قيود-الوصول-بتغيير-حروف-الـ-path-case-sensitivity`  
**Category:** WAF Bypass, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081ea878bc6317c0edbce  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الأنظمة (case-sensitive routing) بتفرق في الرد بين الحروف الكبيرة والصغيرة في الـ path، فلو الـ lowercase محطوط أو محمي، جرّب نفس الـ path بحروف مختلفة (Camel/Mixed case) لأن الـ rule اللي بتمنع الوصول بتكون case-sensitive لكن الـ backend مش case-sensitive.

## Payload / Code

```
target\[.\]com/phpmyadmin/setup/index.php → 301 (راجع للوجن)
target\[.\]com/phpMyAdmin/setup/index.php → 200 (فتح صفحة setup مباشرة!)

phpmyadmin → 301
phpMyAdmin → 200
```

## Source

kjulius @ethical\_h4ck3r\_ — Credit: @GodfatherOrwa

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
