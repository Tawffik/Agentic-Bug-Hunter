# SKILL: GitHub Actions <code>pull_request_target</code> → untrusted PR code executed with secrets

**Skill id:** `tip/github-actions-codepull-request-targetcode-untrusted-pr-code-executed-with-secrets`  
**Category:** RCE, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081e5bc68ff0c11b2ca94  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

pull_request_target يعمل بسياق المستودع الأساسي وقد يملك صلاحيات أو secrets لا يملكها workflow عادي لحدث pull_request. الخطر يظهر عندما يقوم workflow بعد ذلك checkout أو تنفيذ كود/أوامر من PR غير موثوق. راجع ترتيب checkout وتشغيل scripts والـ permissions؛ لا تنفذ كود PR غير موثوق في سياق privileged. أثبت المشكلة في fork أو مختبر تملكه، دون الوصول إلى أسرار مستودع حي.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

GitHub Security Docs — Securely using pull\_request\_target: [https://docs.github.com/en/actions/reference/security/securely-using-pull\_request\_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) ; OpenLIT advisory: [https://github.com/openlit/openlit/security/advisories/GHSA-9jgv-x8cq-296q](https://github.com/openlit/openlit/security/advisories/GHSA-9jgv-x8cq-296q) ; Microsoft Symphony advisory: [https://github.com/microsoft/symphony/security/advisories/GHSA-pq5r-g36r-rpx7](https://github.com/microsoft/symphony/security/advisories/GHSA-pq5r-g36r-rpx7)

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
