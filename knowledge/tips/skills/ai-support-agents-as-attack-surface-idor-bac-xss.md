# SKILL: AI support agents as attack surface (IDOR / BAC / XSS)

**Skill id:** `tip/ai-support-agents-as-attack-surface-idor-bac-xss`  
**Category:** IDOR, Auth Bypass, XSS, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081bab9b8c602dbe52806  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Auth Bypass, XSS, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Companies replace human support with LLM agents that can look up accounts, change details, and issue refunds. Same bug classes with new names: agent shows another user's data = IDOR; agent does admin actions for a normal user = broken access control; unescaped agent output on a page = XSS. Start from OWASP Top 10 for LLM Apps. Prefer two test accounts and clear evidence. Do not auto-confirm from chat text alone.

## Payload / Code

```
Map support/chat/agent endpoints
Prompt injection to request other-user data (authorized tests only)
Compare agent actions with and without session
Check reflected agent HTML sinks
```

## Source

Twitter/X @dd\_pwnd — support chat is part of the attack surface (Nov 2026); \~\$50k reports mentioned with low competition

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
