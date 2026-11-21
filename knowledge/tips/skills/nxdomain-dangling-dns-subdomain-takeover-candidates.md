# SKILL: NXDOMAIN + dangling DNS → subdomain takeover candidates

**Skill id:** `tip/nxdomain-dangling-dns-subdomain-takeover-candidates`  
**Category:** Subdomain Enum, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081928a7ef3da92de5e81  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Subdomain Enum, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

سجلات DNS التي تنحل إلى NXDOMAIN أو CNAME لخدمات متروكة مرشحة لـtakeover. فرّق بين NXDOMAIN الحقيقي وخدمة لا تزال مملوكة للبرنامج. استخدم قوائم can-i-take-over-xyz قبل أي ادعاء، وأثبت التحكم في السجل فقط ضمن قواعد البرنامج.

## Payload / Code

```
subfinder -d [target.com](http://target.com) -silent \| dnsx -a -resp \| grep -i NXDOMAIN
# Also: httpx live check + fingerprint against known vulnerable services
# Validate with: [github.com/EdOverflow/can-i-take-over-xyz](http://github.com/EdOverflow/can-i-take-over-xyz) labels Vulnerable / Edge case
```

## Source

Fardeen A. tip (X) — subfinder \| dnsx NXDOMAIN

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
