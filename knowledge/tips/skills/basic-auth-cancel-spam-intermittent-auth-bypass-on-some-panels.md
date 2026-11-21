# SKILL: Basic Auth cancel spam — intermittent auth bypass on some panels

**Skill id:** `tip/basic-auth-cancel-spam-intermittent-auth-bypass-on-some-panels`  
**Category:** Auth Bypass  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081f491f8eca659c659f1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في بعض لوحات login القديمة، إلغاء نافذة Basic Auth عدة مرات قد يُسقط الجلسة إلى حالة authenticated أو يكشف محتوى محمي بسبب خطأ في منطق التحدي. نادر وغير مضمون؛ وثّق بدقة إن نجح ولا تعتمد عليه كمنهج أساسي.

## Payload / Code

```
Open protected path → browser Basic Auth prompt → Cancel 3–4 times → observe whether body/admin UI leaks.
Prefer reproducing with raw HTTP (empty Authorization / repeated 401 handling) for a clean PoC.
```

## Source

mahmoud tip (X) — cancel basic auth 3–4 times

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
