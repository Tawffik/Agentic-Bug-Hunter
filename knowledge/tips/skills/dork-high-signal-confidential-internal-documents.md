# SKILL: Dork (High Signal): Confidential / Internal documents

**Skill id:** `tip/dork-high-signal-confidential-internal-documents`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081f7944fd48e9ed214d9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بيجيب PDFs و docs داخلية مكشوفة.

## Payload / Code

```
site:[target.com](http://target.com) (filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:csv) (confidential OR "internal use" OR "not for public" OR "do not distribute" OR password OR secret)
```

## Source

Proven document dorks

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
