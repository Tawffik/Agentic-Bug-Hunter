# SKILL: Password Reset Race Condition (OTP / token generation)

**Skill id:** `tip/password-reset-race-condition-otp-token-generation`  
**Category:** Password Reset, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081a38047f59896d70a47  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ابعت طلبات كتير في نفس الوقت لـ OTP أو token generation. أحيانًا بيتولد توكنات متوقعة أو قابلة للتصادم.

## Payload / Code

```
Turbo Intruder / race on /forgot-password or /send-otp
```

## Source

Recent race ATO cases 2026

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
