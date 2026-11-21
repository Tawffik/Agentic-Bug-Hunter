# SKILL: robots.txt + sitemap.xml → hidden sensitive paths

**Skill id:** `tip/robotstxt-sitemapxml-hidden-sensitive-paths`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081e8840efd9daeecc1c0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

مش بس تقرأهم، استخدمهم كـ wordlist. كتير من الـ Disallow بتكون endpoints حساسة أو admin panels أو backup paths.

## Payload / Code

```
curl [https://target.com/robots.txt](https://target.com/robots.txt)
curl [https://target.com/sitemap.xml](https://target.com/sitemap.xml)
# حط الـ paths في ffuf
```

## Source

Classic but still effective (Intigriti BugQuest Day 9)

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
