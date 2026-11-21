# SKILL: Backup files (wp-config.php.bak, .env.bak, .sql, \~ files) → credentials leak

**Skill id:** `tip/backup-files-wp-configphpbak-envbak-sql-files-credentials-leak`  
**Category:** Recon  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880814085f2cb5810d8331d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اكتشاف أسماء ملفات backup مفيد، لكن ليس كل ملف يحتوي credentials ولا كل كشف قابل للدفع. استخدم wordlist على الأصول المصرح بها بمعدل منخفض، وتحقق من نوع الملف ومحتواه بأقل دليل ممكن دون تحميل قواعد بيانات أو استخدام أسرار.

## Payload / Code

```
ffuf -u [https://target.com/FUZZ](https://target.com/FUZZ) -w backup\_wordlist.txt
# أمثلة: wp-config.php.bak, .env.bak, backup.sql, database.sql
```

## Source

Intigriti WordPress guide + Burp labs + common practice

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
