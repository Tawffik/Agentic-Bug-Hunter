# SKILL: Katana JS collection → extract S3 URLs → verify bucket exposure

**Skill id:** `tip/katana-js-collection-extract-s3-urls-verify-bucket-exposure`  
**Category:** Recon, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ccaca0c6855c4a8bc9  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Crawl or collect JS with Katana, extract [amazonaws.com](http://amazonaws.com) / s3 bucket hostnames from scripts and configs, then check whether the bucket allows public list/read (authorized targets only). Often yields backups, uploads, or admin artifacts.

## Payload / Code

```
1) katana -u [https://target.com](https://target.com) -jc -o js\_urls.txt
2) grep -E 's3\[.-\]\|[amazonaws.com](http://amazonaws.com)\|[blob.core.windows](http://blob.core.windows)\|storage.googleapis' js\_and\_pages
3) Normalize bucket names
4) Test public access carefully (list/read only if program allows)

Optional tool (authorized PT/BB only):
[github.com/0xmoot/s3sec](http://github.com/0xmoot/s3sec)
cat buckets.txt \| python3 [s3sec.py](http://s3sec.py)
```

## Source

Mohamed Ahmed — exposed S3 via Katana; HackGit s3sec

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
