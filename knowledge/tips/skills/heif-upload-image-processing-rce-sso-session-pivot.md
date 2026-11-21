# SKILL: HEIF Upload → Image-Processing RCE → SSO Session Pivot

**Skill id:** `tip/heif-upload-image-processing-rce-sso-session-pivot`  
**Category:** RCE, Auth Bypass, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e3dac31e880810286d4c8273d1abc75  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, Auth Bypass, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A recent authorized research chain showed why image-upload endpoints deserve deeper review than simple file-type validation. The initial primitive was a crafted HEIF/HEIC upload reaching a vulnerable native image-processing dependency; the important escalation was the surrounding trust boundary: forum/server compromise plus shared SSO/session handling created a path toward employee accounts and internal developer tooling. The hunting lesson is to test upload processing paths for native parsers, then separately map whether the affected service shares authentication or session trust with higher-value systems. Study Tab: image/attachment upload → test native format processing and version exposure → parser compromise + session/SSO trust boundary → validate only in-scope with harmless proof and stop before sensitive data access. Use when: a target accepts HEIF/HEIC or other complex media formats and the service participates in shared SSO, staff portals, or internal tooling.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Hacktron / The Verge — 18 Sep 2026 — [https://www.theverge.com/ai-artificial-intelligence/997444/openai-hack-claude-heif-heist](https://www.theverge.com/ai-artificial-intelligence/997444/openai-hack-claude-heif-heist)

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
