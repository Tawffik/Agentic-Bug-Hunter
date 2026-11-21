# SKILL: DorkAgent — automate scoped dork research

**Skill id:** `tip/dorkagent-automate-scoped-dork-research`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808119aeb0d65865f0b7e4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

أداة لتجميع/تشغيل عمليات dorking بصورة منظمة. استخدمها فقط على اسم المؤسسة أو النطاقات المصرح بها، وراجع كل نتيجة يدويًا: هل هي أصل حالي؟ هل السر حقيقي أم مثال/fixture؟ هل يوجد دليل على ملكية الهدف؟ لا تستخدم أي credentials مكشوفة.

## Payload / Code

```
Repository: [https://github.com/yee-yore/DorkAgent\\nWorkflow](https://github.com/yee-yore/DorkAgent%5CnWorkflow): define in-scope domain/org → run passive queries → deduplicate results → manually validate → redact secrets in notes.
```

## Source

[https://github.com/yee-yore/DorkAgent](https://github.com/yee-yore/DorkAgent)

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
