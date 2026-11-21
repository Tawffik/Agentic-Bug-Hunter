# SKILL: Pipeline كامل لاكتشاف Subdomain Takeover

**Skill id:** `tip/pipeline-كامل-لاكتشاف-subdomain-takeover`  
**Category:** Subdomain Enum  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081b3bb88c25f1348d2bc  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Subdomain Enum**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

خط أنابيب كامل يجمع الساب دومينز، يفلتر اللي شغالة، ويشغّل nuclei templates متخصصة للتأكد من wجود CNAME دال (dangling) بيشاور على خدمة third-party (GitHub Pages, Heroku, Fastly, Shopify, S3) محدش ممكن تطالبها وتعملها claim.

## Payload / Code

```
subfinder -d [target.com](http://target.com) -o subs.txt
cat subs.txt \| httpx -silent -o live.txt
nuclei -l live.txt -t \~/nuclei-templates/takeovers/ -o takeovers.txt

لو لقيت CNAME دال (dangling)، اعمل claim للـ resource على المنصة التانية وارفع PoC
```

## Source

Redfox Security 2026

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
