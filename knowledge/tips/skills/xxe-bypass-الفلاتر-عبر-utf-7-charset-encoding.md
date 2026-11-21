# SKILL: XXE: Bypass الفلاتر عبر UTF-7 Charset Encoding

**Skill id:** `tip/xxe-bypass-الفلاتر-عبر-utf-7-charset-encoding`  
**Category:** General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081de86aafc1c0718e7c4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

فلاتر الـ XXE بتدور على patterns في UTF-8 بس. لو encode الـ payload بـ UTF-7، الفلتر مش هيعرف الشكل لكن XML parser هيفكّه وينفذه عادي.

## Payload / Code

```
استخدم encoder يحول الـ XXE payload العادي لـ UTF-7 encoding
واضبط الـ XML declaration على: \
ثم ارفع الـ payload المشفر بدل العادي
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 26)

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
