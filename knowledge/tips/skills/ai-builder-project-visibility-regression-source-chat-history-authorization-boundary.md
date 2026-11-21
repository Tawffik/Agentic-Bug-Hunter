# SKILL: AI Builder Project Visibility Regression → Source / Chat History Authorization Boundary

**Skill id:** `tip/ai-builder-project-visibility-regression-source-chat-history-authorization-boundary`  
**Category:** Recon, General  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e8808102bc25fe5995725604  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Official historical evidence: Lovable reported and fixed a regression that exposed public-project chat history/source to other authenticated users with a project link. This supports the general authorization-boundary test idea, but does not establish a currently exploitable bug on Lovable or another product. Since this test needs two controlled accounts/projects and a current in-scope product, keep it as a review lead until a current candidate is independently verified.

## Payload / Code

```
For an explicitly in-scope AI builder or collaboration SaaS, compare permissions between the published app URL, project/editor URL, remix/share links, version history, generated source, and prompt/chat history using two accounts you control. Check whether an ordinary user can access project metadata or conversation history belonging to the second test account. Do not guess private links or access real customers' projects. Avoid retesting the disclosed Lovable regression unless the program explicitly requests verification.
```

## Source

[Lovable official incident response (reported fixed)](https://lovable.dev/blog/our-response-to-the-april-2026-incident) ; [Escape research methodology on vibe-coded apps](https://escape.tech/blog/methodology-how-we-discovered-vulnerabilities-apps-built-with-vibe-coding/)

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
