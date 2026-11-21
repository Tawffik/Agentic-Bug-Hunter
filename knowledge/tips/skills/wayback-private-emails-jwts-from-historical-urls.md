# SKILL: Wayback → private emails / JWTs from historical URLs

**Skill id:** `tip/wayback-private-emails-jwts-from-historical-urls`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e88081e681a9d13318f00143  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الأرشيف التاريخي يحتفظ بمسارات فيها إيميلات داخلية أو JWTs في query/fragment/body قديمة. مش كل نتيجة ثغرة؛ صنّف كـ information disclosure فقط لو البيانات حساسة وما زالت صالحة أو تكشف هيكل داخلي مفيد. اربط النتائج بالنطاق المصرّح وامسح التكرار قبل البلاغ.

## Payload / Code

```
# Private-looking emails from historical surface
cat subs.txt \| waybackurls \| grep -Ei 'gmail\|@\[a-z0-9.-\]+.(com\|io\|net)' \| tee emails\_wayback.txt

# JWTs in archived URLs
cat urls.txt \| grep -Eo 'eyJ\[A-Za-z0-9\_-\]+.\[A-Za-z0-9\_-\]+.\[A-Za-z0-9\_-\]+' \| sort -u
# Decode header/payload on [jwt.io](http://jwt.io) — check alg, kid, exp, roles; never use live tokens abusively
```

## Source

Bug X Hunter + Swartz tips (X)

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
