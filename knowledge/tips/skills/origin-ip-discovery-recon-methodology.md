# SKILL: Origin IP Discovery — Recon Methodology

**Skill id:** `tip/origin-ip-discovery-recon-methodology`  
**Category:** Recon, WAF Bypass  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e0dac31e8808125ac29f7cf4a16d9a7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الهدف هو فهم البنية التي تخدم الأصل من دون افتراض أن عنوان IP المكتشف قابل للاستهداف أو خارج الحماية. قارن سجلات DNS التاريخية والحالية، شهادات TLS، أسماء المضيفين والردود على الأصول المصرح بها؛ تحقق من أن العنوان يعود فعلًا للبرنامج قبل أي اختبار مباشر. لا تحاول تجاوز CDN/WAF أو فحص بنية طرف ثالث غير مدرجة في النطاق.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Professor the Hunter — Origin IP checklist (رابط المنشور الأصلي غير متاح في السجل الحالي). مرجع أداة مكمل للاستطلاع المصرح: OWASP Amass: [https://github.com/owasp-amass/amass](https://github.com/owasp-amass/amass)

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
