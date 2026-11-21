# SKILL: تقنية جديدة لإيجاد الساب دومينز عبر [crt.sh](http://crt.sh) API

**Skill id:** `tip/تقنية-جديدة-لإيجاد-الساب-دومينز-عبر-crtshhttpcrtsh-api`  
**Category:** Subdomain Enum, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e880811c9b18caf4586e1b0f  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Subdomain Enum, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

استخدام Certificate Transparency logs عن طريق endpoint بديل لـ [crt.sh](http://crt.sh) لسحب كل الساب دومينز المسجلة في شهادات SSL الخاصة بالدومين المستهدف بسرعة وبدون scraping.

## Payload / Code

```
[crt.name/v1/search?apex=target.com](http://crt.name/v1/search?apex=target.com)
(مثال: [crt.name/v1/search?apex=microsoft.com](http://crt.name/v1/search?apex=microsoft.com))
```

## Source

cryptoshant 🇮🇳 @cryptoshan484

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
