# SKILL: Git history (not current files) → leaked CI/CD tokens (NASA VDP case)

**Skill id:** `tip/git-history-not-current-files-leaked-cicd-tokens-nasa-vdp-case`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081abbe4af1d13adfdab9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لما تلاقي public GitLab/GitHub org، متكتفيش بالـ current files. clone الـ repo وشغّل gitleaks أو trufflehog على الـ full history. في NASA طلع CI tokens من commits قديمة 2023.

## Payload / Code

```
git clone [https://gitlab.example.com/org/repo](https://gitlab.example.com/org/repo)
cd repo
gitleaks detect --source . -v
# أو trufflehog git [https://app.notion.com](https://app.notion.com).
```

## Source

alaric InfoSec Write-ups – NASA VDP Letter of Recognition (P1)

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
