# SKILL: Exposed Google Maps API keys may unlock Gemini — validate model access not just Maps

**Skill id:** `tip/exposed-google-maps-api-keys-may-unlock-gemini-validate-model-access-not-just-maps`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808163982ce1968850e568  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض مفاتيح Google Maps (AIza…) المنشورة في JS قد تكون مربوطة بمشروع Cloud فيه Gemini/Generative Language مفعّل بدون قيود كافية. وجود المفتاح وحده ليس ثغرة؛ الأثر يبدأ عندما يثبت أن نفس المفتاح يستدعي models أو يتجاوز referrer/API restrictions. ابحث في: JS/source maps، Wayback، Android APKs، web assets. بعد الاستخراج اختبر فقط على نطاق مصرّح ووثّق الـAPI المفعّلة والقيود (HTTP referrer، IP، API restrictions) قبل أي بلاغ.

## Payload / Code

```
Hunt sources: JS bundles, .[js.map](http://js.map), waybackurls, APK strings.
Pattern: AIza\[0-9A-Za-z\_-\]\{35\}
Validate impact (authorized only): try Generative Language / Gemini endpoints if program allows; check Maps quotas vs other Google APIs; document restriction bypass evidence.
Tool mention: geminiHunter (community) for multi-source discovery — treat output as LEAD until impact proven.
```

## Source

Zeroday Lab / geminiHunter tip (X, Nov 2026)

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
