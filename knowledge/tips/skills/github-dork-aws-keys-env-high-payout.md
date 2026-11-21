# SKILL: GitHub Dork: AWS keys + .env (high payout)

**Skill id:** `tip/github-dork-aws-keys-env-high-payout`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880812c8299c4d6f1bf403a  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أقوى تركيبة لـ AWS secrets. استبدل TARGET بالـ org الرسمي.

## Payload / Code

```
org:TARGET ("AWS\_SECRET\_ACCESS\_KEY" OR "AWS\_ACCESS\_KEY\_ID" OR AKIA) (filename:.env OR filename:config)
```

## Source

Intigriti + AllClearDigital 2026

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
