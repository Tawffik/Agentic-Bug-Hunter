# SKILL: humans.txt on filtered 404 subdomains — names and credentials

**Skill id:** `tip/humanstxt-on-filtered-404-subdomains-names-and-credentials`  
**Category:** Recon, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880818a86d9e875e841df72  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

After subfinder + httpx, filter 404 (or odd-status) subdomains and content-discover with ffuf. /humans.txt is an old convention that sometimes still lists developer names, emails, or leftover credential notes.

## Payload / Code

```
subfinder -d [target.com](http://target.com) -silent \| httpx -mc 404 -silent -o 404subs.txt
ffuf -w wordlist.txt -u [https://FUZZ.target.com/humans.txt](https://FUZZ.target.com/humans.txt) -mc 200
# also try path on known 404 host:
[https://sub.target.com/humans.txt](https://sub.target.com/humans.txt)

Add /humans.txt to recon wordlists.
```

## Source

Mohamed Ahmed — Sensitive Information Exposure (humans.txt)

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
