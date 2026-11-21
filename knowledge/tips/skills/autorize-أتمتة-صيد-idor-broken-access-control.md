# SKILL: Autorize — أتمتة صيد IDOR / Broken Access Control

**Skill id:** `tip/autorize-أتمتة-صيد-idor-broken-access-control`  
**Category:** IDOR, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/241f6a4a404b4f79a92f3c0f9a7be9fb  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما تختبر كل endpoint يدوي للـ access control، Autorize بياخد كوكيز مستخدم أقل صلاحية وبيعيد تلقائيًا كل ريكوست بتعمله وانت متصفح بحساب أعلى، وبيقولك لو الـ endpoint اتفتح بصلاحية أقل (Bypassed). نص اكتشافات الـ IDOR بتيجي من تشغيله في الخلفية أثناء التصفح العادي.

## Payload / Code

```
1) سجّل حسابين: low-priv (victim cookies تتحط في Autorize) + high-priv تتصفح بيه
2) حط cookies حساب الـ low-priv في Autorize
3) اتصفح كل فيتشرز الحساب العالي صلاحية عادي
4) Autorize بيعيد كل ريكوست بالكوكيز الأقل صلاحية ويقارن الرد (Enforced/Bypassed!)
```

## Source

Autorize (Burp Extension) — HackByNight Real World Guide 2025

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
