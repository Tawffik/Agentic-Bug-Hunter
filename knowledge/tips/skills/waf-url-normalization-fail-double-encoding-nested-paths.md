# SKILL: WAF URL normalization fail — double encoding & nested paths

**Skill id:** `tip/waf-url-normalization-fail-double-encoding-nested-paths`  
**Category:** WAF Bypass, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e880816ab16ee7f0bd996266  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Some WAFs fail during URL normalization. Double-encoding slashes or inserting nested encoded traversal segments can reach a backend path the WAF thought it blocked. Always compare against a 404 calibration and stay on authorized hosts. Smart 403 in Zero Track now includes these techniques as LEAD probes only.

## Payload / Code

```
/api/v1/%2e%2e/%2e%2e/config
/path%252fadmin
/%252e%252e%252fsecret
MID inserts: /%2e%2e/ , /%252e%252e/
```

## Source

Twitter/X @Omar\_3lsayed — Bug Bounty Tip WAF URL normalization (Dec 2025 style tips circulating 2026)

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
