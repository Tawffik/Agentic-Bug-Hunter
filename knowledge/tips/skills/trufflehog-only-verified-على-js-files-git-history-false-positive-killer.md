# SKILL: TruffleHog --only-verified على JS files + Git history (false-positive killer)

**Skill id:** `tip/trufflehog-only-verified-على-js-files-git-history-false-positive-killer`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081b3b83bf4926912ae08  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اجمع الـ JS أولاً بـ subjs أو Katana، بعدين شغّل trufflehog filesystem ./js\_files --only-verified. الفلاج ده بيتحقق فعليًا من الـ API إن الـ secret لسه شغال، فبيقلل الـ false positives بشكل كبير وبيرفع جودة التقرير.

## Payload / Code

```
subjs -i urls.txt -o js.txt
# حمل الملفات ثم:
trufflehog filesystem ./js\_dir --only-verified
trufflehog github --org=target --only-verified
```

## Source

SecurityCipher + Intigriti secrets guide 2025/2026

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
