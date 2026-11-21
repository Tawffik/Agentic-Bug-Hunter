# SKILL: MCP Cache Poisoning → Cross-User Prompt Injection via Cached Tool Instructions

**Skill id:** `tip/mcp-cache-poisoning-cross-user-prompt-injection-via-cached-tool-instructions`  
**Category:** API Hacking, Auth Bypass, General  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e2dac31e88081128c00ddec87002f70  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **API Hacking, Auth Bypass, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

توضح المقالة سلسلة منطقية داخل MCP: إذا سمح خادم غير موثوق بتعليمات tool أو system-prompt أن تُوسم كـ public-cacheable، ثم أعاد العميل أو البوابة تقديم الاستجابة المخزنة لمستخدمين آخرين، فقد تنتقل تعليمات المهاجم عبر cache من مستخدم واحد إلى عدة مستخدمين. نقطة الاختبار ليست وجود cache وحده، بل هل يمكن إدخال تعليمات يتحكم بها الخادم ثم إثبات أنها تُعاد عبر shared gateway إلى جلسة مستخدم آخر وتؤثر في agent context. Study Tab: MCP tool/list أو instructions responses → اختبر Cache-Control وVary وcache key وshared gateway behavior → poisoned instructions → تحقق من cross-user replay داخل agent context بدون تنفيذ أفعال مؤذية. Use when: التطبيق يستخدم MCP أو gateway مشتركًا مع caching لاستجابات الأدوات أو التعليمات، ويوجد server أو integration غير موثوق يمكنه التأثير في هذه الاستجابات.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Maxime Dalessandro — Datapace — updated 21 Sep 2026 — [https://datapace.ai/blog/mcp-cache-poisoning-prompt-injection](https://datapace.ai/blog/mcp-cache-poisoning-prompt-injection)

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
