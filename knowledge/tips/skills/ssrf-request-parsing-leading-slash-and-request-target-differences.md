# SKILL: SSRF / Request Parsing — leading-slash and request-target differences

**Skill id:** `tip/ssrf-request-parsing-leading-slash-and-request-target-differences`  
**Category:** SSRF, Fuzzing  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/406dac31e880812d95abda81af406208  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Some clients, proxies, or backends parse request targets differently. A leading slash or alternate request-target form can change routing in certain stacks, but the syntax difference alone is not a vulnerability and must not be treated as a universal bypass.

## Payload / Code

```
In an authorized lab or explicitly approved SSRF test, compare one request-format variable at a time and observe only a harmless, controlled callback or expected route. Record the exact client/proxy/backend behavior. Do not probe internal IPs, cloud metadata, or sensitive services unless the program explicitly authorizes that exact testing.
```

## Source

User-provided Orwa screenshot: request-target slash nuance; normalized as a hypothesis, not a confirmed universal technique

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
