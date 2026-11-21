# SKILL: Google Alerts على Dorks الثابتة لمراقبة Exposure جديدة

**Skill id:** `tip/google-alerts-على-dorks-الثابتة-لمراقبة-exposure-جديدة`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081eba6c3dcddbf6db24f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اكتب dork قوي وثابت (site:[target.com](http://target.com) ext:env OR filetype:sql OR "AWS\_SECRET\_ACCESS\_KEY" OR intitle:"index of") وحطه في Google Alerts. كل ما يظهر محتوى جديد بعد deploy أو misconfig هيجيلك إيميل. مثالي للبرامج طويلة الأمد.

## Payload / Code

```
مثال Alerts:
site:[target.com](http://target.com) (ext:env OR ext:sql OR ext:bak OR "DB\_PASSWORD")
site:[target.com](http://target.com) filetype:pdf "confidential"
```

## Source

Hunter practice + Intigriti recon series

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
