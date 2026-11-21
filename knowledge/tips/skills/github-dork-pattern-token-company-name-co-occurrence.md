# SKILL: GitHub dork pattern: Token / Company name co-occurrence

**Skill id:** `tip/github-dork-pattern-token-company-name-co-occurrence`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081fbbb4cf96d03c02eed  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Hardcoded secrets often appear near company or product names. Searching for Token= (or similar) together with the company name surfaces config snippets and scripts that generic org-only searches miss. Verify ownership and do not use any token found.

## Payload / Code

```
GitHub Code Search examples (replace Company):
"Token=" "CompanyName"
"token=" "CompanyName"
"api\_key" "CompanyName"
"client\_secret" "CompanyName"

Also:
"CompanyName" filename:.env
"CompanyName" "AWS\_SECRET\_ACCESS\_KEY"
```

## Source

Mohamed Ahmed — GitHub dork reply (Token= Company name)

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
