# SKILL: Bypass File Upload Validation بـ Magic Bytes

**Skill id:** `tip/bypass-file-upload-validation-بـ-magic-bytes`  
**Category:** General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081ef9c1ef987b59794ff  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الأنظمة بتتحقق من أول بايتات فقط في الملف المرفوع (Magic Bytes/File Signature) بدون ما تفحص كل الملف. لو حطيت Magic Bytes بتاعة PNG/JPG في أول الملف وبعدين حطيت كود ضار (webshell)، الفاليديشن بتعدية بتقبله — ويتنفّذ لو السيرفر بيمشيه بامتداد الملف الأصلي.

## Payload / Code

```
مثال: ابدأ الملف بـ magic bytes PNG (x89PNGrnx1an) ثم ضيف كود الـ PHP shell بعدين
دمجها مع double extension: shell.png.php أو content-type manipulation لنتيجة أقوى
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 19)

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
