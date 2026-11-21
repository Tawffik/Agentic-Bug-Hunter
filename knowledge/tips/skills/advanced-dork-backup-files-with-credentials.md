# SKILL: Advanced Dork: Backup files with credentials

**Skill id:** `tip/advanced-dork-backup-files-with-credentials`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880813baaabd6519b3225c1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الـ dork قد يجد ملفات backup مفهرسة، لكن نتائج البحث قد تكون قديمة أو أمثلة أو خارج النطاق. تحقق من وجود الملف واستجابة الخادم دون تنزيل dumps أو أسرار. أضف رابط مصدر محدد يثبت الطريقة بدل الاكتفاء بعبارة multiple guides.

## Payload / Code

```
site:[target.com](http://target.com) (ext:bak OR ext:old OR ext:backup OR ext:\~ OR ext:swp) (password OR secret OR key OR db\_)
```

## Source

Undercode + multiple guides

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
