# SKILL: Azure DevOps Public Project Review → Pipeline Metadata & Accidental Secret Exposure

**Skill id:** `tip/azure-devops-public-project-review-pipeline-metadata-accidental-secret-exposure`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081e580a3d791cbe618fd  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Public Azure DevOps projects and repository/build surfaces may expose pipeline YAML, build logs, test outputs, artifacts, deployment configuration, or identifiers that reveal how a target deploys. The highest-signal angle is accidental disclosure inside an artifact or log (for example, a credential accidentally printed in a failed build), not simply finding a public project. This is distinct from GitHub Actions workflow injection already covered in Notion. Public-project visibility can be intentional, and program policies differ sharply.

## Payload / Code

```
Passive-first, in-scope workflow: identify the organization's official Azure DevOps tenant from public references; inspect only publicly accessible project/repository/build pages and artifacts; review pipeline YAML, recent failed-build logs, test reports, coverage output, and downloadable build artifacts for secrets or private deployment data. Do not guess or access private project IDs, use stolen credentials, trigger builds, or test credentials against live services. If a suspected secret appears, capture a redacted proof and report it; do not use it.
```

## Source

[https://www.microsoft.com/en-us/msrc/bounty-azure-devops](https://www.microsoft.com/en-us/msrc/bounty-azure-devops) ; [https://microsoft.github.io/zerotrustassessment/docs/workshop-guidance/devsecops/DS\_076](https://microsoft.github.io/zerotrustassessment/docs/workshop-guidance/devsecops/DS_076) ; [https://bugbounty.info/Attack-Surface/CI-CD/Secret-Leakage](https://bugbounty.info/Attack-Surface/CI-CD/Secret-Leakage)

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
