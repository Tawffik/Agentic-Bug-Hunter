# SKILL: ScreenConnect Application Logs — Reconstruct Remote Session Activity

**Skill id:** `tip/screenconnect-application-logs-reconstruct-remote-session-activity`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e0dac31e8808109a8f1ea871b38f4e7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة دفاعية/استطلاعية: سجلات Windows Application قد توضح اتصال ScreenConnect وفصله ونقل الملفات أو تنفيذ أوامر، فتساعد على بناء timeline وربط نشاط غير متوقع بوجهة relay أو خدمة مثبتة. راجع Event Viewer واحتفظ بالسجلات مع الوقت ومصدر الحدث؛ لا تعتبر event ID وحده دليل اختراق، وقارنه بجرد أدوات الدعم المصرح بها وبسياق الجهاز.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Ayush Anand (@Securityinbits) — 2026. مرجع توثيقي مكمل: ConnectWise ScreenConnect Intruder Alert Checklist: [https://www.screenconnect.com/siteassets/media/assets/docs/connectwise-screenconnect-intruder-alert-checklist.pdf](https://www.screenconnect.com/siteassets/media/assets/docs/connectwise-screenconnect-intruder-alert-checklist.pdf) ; RULER event-log reference: [https://ruler-project.github.io/RULER/remote/Connectwise\_Screenconnect/](https://ruler-project.github.io/RULER/remote/Connectwise_Screenconnect/)

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
