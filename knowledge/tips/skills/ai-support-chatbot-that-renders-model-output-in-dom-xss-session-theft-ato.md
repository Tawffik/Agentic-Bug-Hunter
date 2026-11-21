# SKILL: AI support chatbot that renders model output in DOM → XSS → session theft / ATO

**Skill id:** `tip/ai-support-chatbot-that-renders-model-output-in-dom-xss-session-theft-ato`  
**Category:** XSS, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081d0870dd69de9db60d4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **XSS, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

شركات كثيرة تضيف chatbot دعم بدون تدقيق مخرجات النموذج. لو البوت يفك payload (base64/URL-decode) ويعرض الناتج في DOM بدون sanitization، تحصل على XSS مخزّن أو منعكس عبر قناة المحادثة. سلسلة شائعة: XSS → سرقة cookies/tokens أو OAuth cookie-downgrade → account takeover. القاعدة: أي مخرجات LLM تُرسَم في الصفحة = سطح هجوم. اختبر على برامج مصرّح بها فقط، بأدلة (request/response + DOM proof) من غير إضرار بالمستخدمين.

## Payload / Code

```
1) Find in-scope AI/chat/support endpoints
2) Send encoded XSS (base64, HTML entities, markdown that becomes HTML)
3) Confirm bot decodes and DOM reflects/executes
4) Escalate only with proof: cookie access, token leak, or auth action in same origin
Heuristic: "If it renders in the DOM, treat it as injectable until proven sanitized."
```

## Source

Patrickbatman writeup tip (X) — AI bot decoded base64 XSS into DOM

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
