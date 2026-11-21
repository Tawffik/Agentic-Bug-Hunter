# SKILL: صيد الأسرار (Secrets) بـ TruffleHog / gitleaks في JS والريبوز

**Skill id:** `tip/صيد-الأسرار-secrets-بـ-trufflehog-gitleaks-في-js-والريبوز`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/2c51eb769beb4fc9a090dcc677a65ea9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

المفتاح هو --only-verified: TruffleHog مبيقولش ده secret إلا لما يجرّبه فعلًا على الـ API ويلاقيه شغّال (يقلل الـ false positives للأدنى). AWS/GCP keys، Stripe، Slack tokens، ومفاتيح دفع مكشوفة في ملفات JS أو ريبوز GitHub قديمة بتدفع باونتي جامد. ركّز على verified بس وقدّم بإثبات تأثير واضح.

## Payload / Code

```
trufflehog github --org=target --only-verified
trufflehog filesystem ./js\_files --only-verified
# اجمع كل ملفات JS الأول
subjs -i urls.txt \| tee js.txt ; cat js.txt \| while read u; do curl -s $u -o "downloaded/$(echo \$u\|md5sum\|cut -d' ' -f1).js"; done
# دور على verified secrets بس عشان تقلل FP
```

## Source

SecurityCipher — Secrets That Pay (TruffleHog) 2026

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
