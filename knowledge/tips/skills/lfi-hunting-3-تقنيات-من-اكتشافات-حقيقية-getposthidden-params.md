# SKILL: LFI Hunting — 3 تقنيات من اكتشافات حقيقية (GET/POST/Hidden Params)

**Skill id:** `tip/lfi-hunting-3-تقنيات-من-اكتشافات-حقيقية-getposthidden-params`  
**Category:** Fuzzing, General  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3ffdac31e88081cbb844cd43710c32a1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

ثلاث طرق مجرّبة لصيد LFI: 1) GET path injection عبر تكرار ../ في أي باراميتر مسار. 2) POST-based LFI في endpoints مش متوقعة زي صفحات router. 3) Hidden parameters تحتاج استخراج بأداة أو مراجعة ملفات JS يدويًا. لتجاوز الفلاتر البسيطة استخدم ترميز بديل للنقطتين والسلاش بدل الشكل العادي.

## Payload / Code

```
GET: ///../../../../etc/passwd
POST: router.jsp?../etc/passwd
Bypass encoding: %2e%2f أو %00 بدل النقطتين العاديتين
```

## Source

MahMoud Elkot — Twitter screenshot, 16 Apr 25 (رد LFI حقيقي موثّق في الصورة)

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
