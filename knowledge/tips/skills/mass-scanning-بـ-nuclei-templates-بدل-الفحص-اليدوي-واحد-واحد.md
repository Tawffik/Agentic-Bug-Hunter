# SKILL: Mass Scanning بـ Nuclei Templates بدل الفحص اليدوي واحد واحد

**Skill id:** `tip/mass-scanning-بـ-nuclei-templates-بدل-الفحص-اليدوي-واحد-واحد`  
**Category:** Recon, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Done  
**Notion:** https://app.notion.com/p/3ffdac31e88081b49c67e5dbdf228aff  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما تدوّر على ثغرة معينة (زي Log4j JNDI RCE) يدويًا على كل أصل لوحده, استخدم قالب Nuclei جاهز ومعروف وشغّله على مئات العناوين دفعة واحدة. الفكرة قابلة للتطبيق على أي CVE أو pattern تاني عندك template جاهز ليه — نتيجة الفحص الجماعي بترجّع كل الأصول المتأثرة فعليًا في طلب واحد بدل عشرات الطلبات اليدوية.

## Payload / Code

```
nuclei -t \ -l targets.txt -o results.txt
```

## Source

MahMoud Elkot — Twitter screenshot, 15 Jul 22 (PoC حقيقي مبني على template @johnk3r لـ OpenNMS Log4j)

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
