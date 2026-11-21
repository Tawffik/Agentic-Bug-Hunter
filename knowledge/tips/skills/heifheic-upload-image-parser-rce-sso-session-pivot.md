# SKILL: HEIF/HEIC Upload → Image Parser RCE → SSO Session Pivot

**Skill id:** `tip/heifheic-upload-image-parser-rce-sso-session-pivot`  
**Category:** RCE, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e4dac31e880817598bad02233ba99bb  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

اختبر مسارات رفع الصور التي تقبل HEIF/HEIC أو تعالجها عبر مكتبات native مثل libheif/ImageMagick. في بحث Hacktron، أدت صورة خبيثة إلى heap overflow وRCE في خدمة المنتدى، ثم استُخدمت جلسات/توكنات تسجيل الدخول المشتركة للوصول إلى حسابات موظفين وخدمات مرتبطة. الفكرة القابلة لإعادة الاستخدام: لا تتوقف عند إثبات crash أو parser bug؛ راقب هل خدمة المعالجة تملك وصولًا إلى session tokens أو SSO أو تكاملات داخلية.nnStudy Tab: upload/image processing endpoint → test HEIF/HEIC parser boundary in an authorized lab or program scope → parser memory-corruption primitive → validate only with a harmless marker and document whether tokens/SSO boundaries are reachable.nnUse when: البرنامج يملك منتدى/دردشة/نظام تذاكر أو أي ميزة ترفع صورًا وتستخدم مكتبات native، خصوصًا إذا كانت مرتبطة بـSSO أو خدمات داخلية.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Hacktron AI — Hacking OpenAI (13 Sep 2026): [https://www.hacktron.ai/blog/hacking-openai](https://www.hacktron.ai/blog/hacking-openai) ; X summary: [https://x.com/HacktronAI/status/2100795824812777893](https://x.com/HacktronAI/status/2100795824812777893)

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
