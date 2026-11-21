# SKILL: Malicious Extension → AI Browser Agent Privilege Hijacking

**Skill id:** `tip/malicious-extension-ai-browser-agent-privilege-hijacking`  
**Category:** General, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e1dac31e88081689862ecfe09935651  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

عند اختبار browser-integrated AI assistants، لا تركز فقط على prompt injection داخل الصفحة؛ افحص أيضًا هل extension مثبتة تستطيع استدعاء أو توجيه agent المدمج في المتصفح عبر نفس صلاحيات جلسة المستخدم. ابحث عن مسار يجعل extension تتحكم في قرارات agent أو browser automation بدون تفاعل إضافي بعد التثبيت، ثم اختبر هل agent يقرأ بيانات حساسة أو ينفذ أفعالًا نيابةً عن المستخدم ضمن صلاحياته. المصدر وثّق نمطًا عابرًا لعدة Chromium-based assistants، لكن شرط التثبيت المسبق للامتداد مهم ويجب اعتباره في threat model.nnStudy Tab: browser AI assistant + extension APIs → اختبر message/command path من extension إلى agent مع جلسة مستخدم مفعلة → agent privilege abuse → أثبت وصولًا لبيانات حساسة أو تنفيذ action غير متوقع.nUse when: المنتج يدمج AI assistant داخل المتصفح أو browser automation ويقبل extensions أو add-ons ذات صلاحيات واسعة.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Gal Weizman / Forever Security — BragJack — 19 Sep 2026 — [https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/)

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
