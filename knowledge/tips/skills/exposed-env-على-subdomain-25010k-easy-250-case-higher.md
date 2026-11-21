# SKILL: Exposed .env على subdomain = \$250–\$10k+ (Easy \$250 case + higher)

**Skill id:** `tip/exposed-env-على-subdomain-25010k-easy-250-case-higher`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081bd824fdb79a668366e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعد subfinder + httpx، شغّل ffuf/dirsearch على .env و .env.backup و .env.local. في حالة exam proctoring موقع طلع .env وخد \$250. في fintech طلع Stripe + AWS = آلاف.

## Payload / Code

```
ffuf -u [https://FUZZ.target.com/.env](https://FUZZ.target.com/.env) -w subs.txt -mc 200
dirsearch -u [https://sub.target.com](https://sub.target.com) -e env,bak,sql -t 30
```

## Source

Abhijeet Kumawat writeup (\$250) + multiple fintech cases \$500–\$10k+

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
