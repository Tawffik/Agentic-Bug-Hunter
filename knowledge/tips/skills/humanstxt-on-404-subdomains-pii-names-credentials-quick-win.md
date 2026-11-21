# SKILL: humans.txt on 404 subdomains → PII / names / credentials (quick win)

**Skill id:** `tip/humanstxt-on-404-subdomains-pii-names-credentials-quick-win`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ccb98cfb77885b89d0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعد Subfinder + httpx على subdomains، استخدم ffuf أو httpx -path /humans.txt على اللي بيرجع 404 أو filtered. كتير من الـ subdomains القديمة أو المهملة بتسيب humans.txt فيها أسماء موظفين، إيميلات، وأحيانًا credentials أو internal notes. سهل جدًا وبيجيب PII سريع.

## Payload / Code

```
cat subs.txt \| httpx -path /humans.txt -mc 200 -o humans.txt
أو ffuf -w subs.txt -u [https://FUZZ.target.com/humans.txt](https://FUZZ.target.com/humans.txt) -mc 200
```

## Source

Mohamed Ahmed writeup (Feb 2025) + common hunter practice

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
