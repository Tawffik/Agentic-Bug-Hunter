# SKILL: Dork (Lesser-known): Bing IP-based search for exposed files

**Skill id:** `tip/dork-lesser-known-bing-ip-based-search-for-exposed-files`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081028ab2c07da1dc42f0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Bing بيدعم ip: وده Google مش بيعمله. لو عندك IP للـ target، دور على الملفات المكشوفة عليه.

## Payload / Code

```
ip:TARGET\_IP (filetype:env OR filetype:sql OR filetype:bak OR filetype:log OR "DB\_PASSWORD")
```

## Source

Medium 2026 - Bing advantage over Google

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
