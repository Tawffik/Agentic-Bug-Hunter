# SKILL: Vhost Fuzzing بـ FFUF — لقاء أصول مخفية

**Skill id:** `tip/vhost-fuzzing-بـ-ffuf-لقاء-أصول-مخفية`  
**Category:** Fuzzing, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081af8c2dfefc391e3a9f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير من الأصول (virtual hosts) بتكون موجودة على نفس الـ IP لكن مش مسجلة في الـ DNS العام. بتجرّب قيم مختلفة لـ Host header عشان تكشف assets محدش محدش تاخدت اهتمام أقل.

## Payload / Code

```
ffuf -u [https://\$TARGET](https://$TARGET) -H "Host: FUZZ.\$TARGET" -w /path/to/wordlist

بعدكده: فلتر على الـ status code / content-length المختلف لتلاقي الـ hosts الشغالة
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 2)

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
