# SKILL: Google-indexed PDFs with personal fields → ID-style parameter tampering

**Skill id:** `tip/google-indexed-pdfs-with-personal-fields-id-style-parameter-tampering`  
**Category:** IDOR, Recon  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ee8efbcf7b4e5a5b8e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Dorks that find PDFs containing fields like date of birth can reveal document endpoints. An ID in the URL may allow sequential access to other records if authorization is missing. Confirm impact carefully and stop once sensitive third-party data is confirmed.

## Payload / Code

```
site:target. "date of birth" ext:pdf
site:[target.com](http://target.com) filetype:pdf "date of birth"
site:[target.com](http://target.com) filetype:pdf "national id"

If URL has id= / doc= / file= → test neighboring IDs only within policy.
Report IDOR/broken access with minimal redacted samples.
```

## Source

Mohamed Ahmed — Unauthenticated Access via Google Dorking (PDF)

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
