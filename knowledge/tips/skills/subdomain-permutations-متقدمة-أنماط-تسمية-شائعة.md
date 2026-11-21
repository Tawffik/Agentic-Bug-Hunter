# SKILL: Subdomain Permutations متقدمة — أنماط تسمية شائعة

**Skill id:** `tip/subdomain-permutations-متقدمة-أنماط-تسمية-شائعة`  
**Category:** Subdomain Enum, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e8808185a3d5f6ecbabcf111  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Subdomain Enum, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كل نمط بيعكس طريقة تسمية مختلفة، وكل واحد فيهم ممكن يطلعلك نتيجة الباقي مبيطلعهاش. ولو ثغرة اتصلحت في الساب دومين الرئيسي، دايمًا فتّش على نسخ تانية منه — بيئات الـ staging والـ dev غالبًا بتفضل غير مصلحة لأسابيع بعد ما الإصلاح يوصل للإنتاج.

## Payload / Code

```
[admin-FUZZ.target.com](http://admin-FUZZ.target.com) → [admin-stg.target.com](http://admin-stg.target.com), [admin-dev.target.com](http://admin-dev.target.com)
[FUZZ-admin.target.com](http://FUZZ-admin.target.com) → [vpn-admin.target.com](http://vpn-admin.target.com), [api-admin.target.com](http://api-admin.target.com)
[adminFUZZ.target.com](http://adminFUZZ.target.com) → [admintest.target.com](http://admintest.target.com), [adminnew.target.com](http://adminnew.target.com)
[FUZZadmin.target.com](http://FUZZadmin.target.com) → [devadmin.target.com](http://devadmin.target.com), [oldadmin.target.com](http://oldadmin.target.com)
[admin.FUZZ.target.com](http://admin.FUZZ.target.com) → [admin.dev.target.com](http://admin.dev.target.com), [admin.staging.target.com](http://admin.staging.target.com)
```

## Source

Intigriti @intigriti — Tips by @GodfatherOrwa (Permutations)

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
