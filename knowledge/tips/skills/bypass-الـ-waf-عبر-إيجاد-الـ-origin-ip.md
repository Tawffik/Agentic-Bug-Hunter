# SKILL: Bypass الـ WAF عبر إيجاد الـ Origin IP

**Skill id:** `tip/bypass-الـ-waf-عبر-إيجاد-الـ-origin-ip`  
**Category:** WAF Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081339863fa2570afa70d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كتير من المواقع مخبية ورا Cloudflare أو WAF تاني. لو لقيت IP السيرفر الأصلي (origin) من سجلات DNS قديمة أو certificate transparency logs (قبل ما يطبقوا الـ protection)، تقدر تتعامل مع السيرفر مباشرة بدون ما الـ WAF يشوف أي payload.

## Payload / Code

```
1) دور على الـ IP الأصلي في [crt.sh](http://crt.sh) أو سجلات قديمة (SecurityTrails, ViewDNS)
2) ارفع الـ request مباشرة للـ IP مع Host header = [target.com](http://target.com)
3) لو السيرفر رد عليك، اختبر الـ payloads مباشرة بدون ما يتفلتر من الـ WAF
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 10)

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
