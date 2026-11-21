# SKILL: GitHub Actions cache poisoning across low-trust and privileged workflows

**Skill id:** `tip/github-actions-cache-poisoning-across-low-trust-and-privileged-workflows`  
**Category:** RCE, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808115952be82b00ea5413  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

_See payload and source for technique details._

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

GitHub Docs — Dependency caching reference: [https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) ; GitHub Changelog (2026-06-26): [https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers/](https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers/) ; CVE-2026-45321: [https://www.cve.org/CVERecord?id=CVE-2026-45321](https://www.cve.org/CVERecord?id=CVE-2026-45321)

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
