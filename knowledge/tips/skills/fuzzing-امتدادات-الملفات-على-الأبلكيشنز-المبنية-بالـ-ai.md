# SKILL: Fuzzing امتدادات الملفات على الأبلكيشنز المبنية بالـ AI

**Skill id:** `tip/fuzzing-امتدادات-الملفات-على-الأبلكيشنز-المبنية-بالـ-ai`  
**Category:** Fuzzing, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e8808167b434e22210c2d952  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير من الويب أبس اللي مبنية بالـ AI بتسيب ملفات .md وملفات تانية زي DB dumps أو env files ظاهرة. الفزّينج بامتدادات كتير بياخد وقت بس بيطلع نتائج قوية.

## Payload / Code

```
ffuf -w /wordlist -u [target.com/FUZZ](http://target.com/FUZZ) -e .md,.db,.txt,.xml,.sql,.7z,.zip,.tar.gz,.env
```

## Source

Godfather Orwa 🇯🇴 @GodfatherOrwa

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
