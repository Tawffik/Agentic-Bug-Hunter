# SKILL: Stored Prompt Injection عبر Project Invite → Cross-User Code Execution

**Skill id:** `tip/stored-prompt-injection-عبر-project-invite-cross-user-code-execution`  
**Category:** Auth Bypass, API Hacking, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e1dac31e88081d9b08ed5a12d18bfbc  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

في تطبيقات الـAI agents اللي بتشغّل shell/browser داخل VM، اختبر هل حقول التعليمات المشتركة (مثل project instructions أو system-like config يحددها مالك المشروع) يتم تحميلها تلقائيًا داخل سياق كل عضو كأنها تعليمات موثوقة. الفكرة العملية: أنشئ مشروعًا/مساحة مشتركة بحساب اختبار، ضع instruction غير مؤذٍ يطلب جلب مورد خارجي، ثم راقب هل agent عضو آخر ينفذها بصلاحيات sandbox الخاصة به. قيمة السلسلة ظهرت عندما تحولت التعليمات المخزنة إلى تنفيذ كود داخل بيئة مستخدم آخر ثم قراءة أسرار البيئة والتحكم في سطح remote desktop؛ لا تعتبر وجود prompt injection وحده ثغرة بدون إثبات cross-user execution أو secret/privilege impact.nnStudy Tab: shared projects / invitation flows / agent instructions → اختبر هل تعليمات المالك تُحقن في كل جلسة عضو كـtrusted config → stored prompt injection → أثبت تنفيذًا داخل sandbox مستخدم آخر مع impact مضبوط.nUse when: التطبيق يدعم shared projects أو team workspaces والـagent يملك shell أو browser أو filesystem أو secrets داخل بيئة تنفيذية.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

CodeAnt AI Security Research Team — 19 Sep 2026 — [https://codeant.ai/security-research/manus-prompt-injection-attack-desktop-takeover](https://codeant.ai/security-research/manus-prompt-injection-attack-desktop-takeover)

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
