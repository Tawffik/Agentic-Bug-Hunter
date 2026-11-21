# SKILL: متستشوششي من Hosts اللي بتعمل Redirect من الـ Root

**Skill id:** `tip/متستشوششي-من-hosts-اللي-بتعمل-redirect-من-الـ-root`  
**Category:** Recon, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e8808140a903cff3eb1ba6b4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو لقيت subdomain بيعمل redirect فورًا من الـ root، متسيبوشه — ده مش معناه إن مفيش حاجة تانية. اعمل fuzzing على الـ paths جواه لأن ملفات وصفحات كتير ممكن تفضل متاحة وغير محمية حتى لو الـ root بتعمل redirect.

## Payload / Code

```
ffuf -u [https://sub.target.com/FUZZ](https://sub.target.com/FUZZ) -w wordlist.txt -mc all -fc 301,302 (فلتر الـ redirects لتلاقي الـ paths الحقيقية)
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 6)

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
