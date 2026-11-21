# SKILL: Recon: فلترة الـ endpoints للصور — طريقة للقاء PII مسربة

**Skill id:** `tip/recon-فلترة-الـ-endpoints-للصور-طريقة-للقاء-pii-مسربة`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880817293efd5154386852f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما تدوّر endpoint بتاع صور واحدة، اعمل recon شامل لكل الـ endpoints اللي بترجع صور (jpg/jpeg/png)، فلترهم لللي shغالة (live) وابعتهم لأداة screenshot. لو لقيت ملف صورة على endpoint معين جرّب تشوف هل الـ directory listing فاتح على الـ folder الأصلي — ممكن تلاقي كمية كبيرة من PII زي passports وهويات.

## Payload / Code

```
1) cat endpoints.txt \| egrep 'jpg\|jpeg\|png' > results.txt
2) filter to live (httpx مثلاً)
3) send results لأداة screenshot

مثال واقعي:
app\[.\]com/xxxx/cdn/file/xxx.jpg → لقى فيه passport
visit app\[.\]com/xxxx/cnd/ → dir listing open → طلعت إيديوها أخلاق PII

(تذكير: 95% من الهانترز بيتجاهلوا وبيشيلوا الـ endpoints بتاعة الصور)
```

## Source

kjulius @ethical\_h4ck3r\_

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
