# SKILL: Third-party AI Chat Widget IDOR → Sensitive Contact / PII Exposure

**Skill id:** `tip/third-party-ai-chat-widget-idor-sensitive-contact-pii-exposure`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880817faa38c5557ee51203  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ dashboard بيبعت requests لـ third-party AI widget domain. جرب IDOR على /widget/contact/upsert أو مشابه بإيميل تاني. بيرجع name, phone, role, internal user/org IDs بدون authorization مناسب. Impact عالي على PII.

## Payload / Code

```
POST /backend/widget/contact/upsert
\{"email": "[victim@example.com](mailto:victim@example.com)"\}
```

## Source

Priyanshu Parmar writeup (Oct 2026) - infosecwriteups

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
