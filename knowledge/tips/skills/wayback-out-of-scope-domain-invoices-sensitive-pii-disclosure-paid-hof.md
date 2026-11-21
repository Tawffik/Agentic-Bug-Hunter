# SKILL: Wayback + out-of-scope domain invoices → Sensitive PII Disclosure (paid + HoF)

**Skill id:** `tip/wayback-out-of-scope-domain-invoices-sensitive-pii-disclosure-paid-hof`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880812f85f0e0623a0a2a8b  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

domain out-of-scope بس الـ invoices كانت public. استخدم waybackurls على الـ short domain، grep على /v/، لقيت mobile + email + payment info. الشركة دفعت ودخلته HoF.

## Payload / Code

```
echo short.domain \| waybackurls \| grep /v/
```

## Source

Rushikesh Chaudhari Medium writeup – paid + Hall of Fame

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
