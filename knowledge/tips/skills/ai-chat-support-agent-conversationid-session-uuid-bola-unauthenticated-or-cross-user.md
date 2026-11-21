# SKILL: AI Chat / Support Agent — conversationID / session UUID BOLA (unauthenticated or cross-user)

**Skill id:** `tip/ai-chat-support-agent-conversationid-session-uuid-bola-unauthenticated-or-cross-user`  
**Category:** IDOR, API Hacking, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081fa8646ec13e3a6156c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

AI assistants and support agents assign conversation or session UUIDs. GraphQL/REST resolvers frequently skip ownership and even authentication checks on history/read endpoints. Swap the conversationID (from URL, body, or WebSocket) with another user's; also test completely unauthenticated. Leaks private prompts, PII, booking details, or internal tool actions. Low competition surface in 2026.

## Payload / Code

```
POST /graphql
\{"query":"query \{ papayaConversationHistory(conversationID: "victim-uuid") \{ messages \} \}"\}

Or REST:
GET /api/chat/history?conversationId=victim-uuid
(without auth header)
```

## Source

Twitter/X @Bug\_Breakdown + @dd\_pwnd — unauthenticated GraphQL IDOR on AI chat history + support agents as attack surface (Nov 2026)

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
