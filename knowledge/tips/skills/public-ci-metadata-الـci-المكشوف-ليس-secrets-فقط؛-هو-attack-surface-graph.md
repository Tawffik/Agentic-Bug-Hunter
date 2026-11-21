# SKILL: 🏗️ Public CI Metadata — الـCI المكشوف ليس Secrets فقط؛ هو Attack-Surface Graph

**Skill id:** `tip/public-ci-metadata-الـci-المكشوف-ليس-secrets-فقط؛-هو-attack-surface-graph`  
**Category:** Recon, General  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e88081798a47c1d4da2d7326  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: public CI/build systems قد تكشف repository, branch, commit, artifact, runner, environment, internal URLs وأحيانًا credentials.

فتّش عن:
Jenkins / Travis / Buildkite / GitLab CI / public Actions artifacts / other exposed build surfaces.

استخرج العلاقات: job → repo → commit → artifact → host/environment.

مثال bounty حقيقي: تقارير HackerOne تضمنت public CI/Jenkins exposure وتسريب GitHub tokens من CI logs.

لا تعرض credential في التقرير الداخلي كنص كامل؛ خزّن evidence آمنًا وقلّل exposure أثناء البحث.

## Payload / Code

```
CI
→ job
→ repo/commit
→ artifact/log
→ internal host/credential candidate
```

## Source

HackerOne disclosed reports — public CI/Jenkins exposure and CI-log credential cases

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
