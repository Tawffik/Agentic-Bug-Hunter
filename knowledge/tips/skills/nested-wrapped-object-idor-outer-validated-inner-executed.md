# SKILL: Nested / Wrapped Object IDOR — outer validated, inner executed

**Skill id:** `tip/nested-wrapped-object-idor-outer-validated-inner-executed`  
**Category:** IDOR, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808119b5b3d27b9356b379  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Auth middleware often validates only the top-level key. Business logic then follows nested objects. Send \{"Account": \{"Account": victimId\}\} or deeper nesting. The outer key passes ownership check; the inner value is used for the actual operation. Scanners almost never test this shape.

## Payload / Code

```
Original: \{"Account": 1111\}
Wrapped:  \{"Account": \{"Account": 3333\}\}

Also try:
\{"user": \{"id": victim\}\}
\{"data": \{"object": \{"id": victim\}\}\}
```

## Source

Twitter/X @vuln\_X — Don't just swap IDs — wrap them (May 2026, high engagement)

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
