# SKILL: GitHub Dork: OpenAI / Anthropic / Slack tokens

**Skill id:** `tip/github-dork-openai-anthropic-slack-tokens`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e880817cb609fea937b02c4b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مفاتيح AI و Slack بتجيب باونتي بسهولة لو first-party.

## Payload / Code

```
org:TARGET ("sk-" OR "sk-ant-" OR "xoxb-" OR "xoxp-" OR "ANTHROPIC\_API\_KEY" OR "OPENAI\_API\_KEY")
```

## Source

Intigriti secrets guide 2025-2026

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
