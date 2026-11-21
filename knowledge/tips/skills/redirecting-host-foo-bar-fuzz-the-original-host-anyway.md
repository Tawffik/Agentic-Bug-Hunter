# SKILL: Redirecting host (foo → bar) → fuzz the original host anyway

**Skill id:** `tip/redirecting-host-foo-bar-fuzz-the-original-host-anyway`  
**Category:** Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880810fa191f8013742378d  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو host بيعمل redirect فوري لدومين تاني، متسيبهوش. اعمل content discovery على الـ original host نفسه (قبل الـ redirect). كتير بيلاقي .git أو configs أو backup files.

## Payload / Code

```
ffuf -u [https://redirecting-host.target.com/FUZZ](https://redirecting-host.target.com/FUZZ) -w wordlist.txt -mc 200,301,302,403 -fs 0
```

## Source

Book of BugBounty Tips

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
