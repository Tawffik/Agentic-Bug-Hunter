# SKILL: Connectivity Check → cURL Shell Injection; Then Pivot to Sibling Features

**Skill id:** `tip/connectivity-check-curl-shell-injection-then-pivot-to-sibling-features`  
**Category:** RCE, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081ad9bcedf8c3fcaf2de  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A recent disclosed-research roundup highlighted a command-injection chain in which a connectivity-check feature passed a user-supplied URL to cURL through a shell; a second feature reused the same risky path. The practical hunting signal is any “test URL”, webhook connectivity check, fetch preview, or network diagnostic that shells out to curl/wget. If one instance is confirmed, inspect other in-scope features that share the same backend helper or implementation instead of stopping at the first entry point.

## Payload / Code

```
Authorized, low-impact workflow:
1. Identify a URL/connectivity-test feature and determine whether errors or timing indicate a shell invocation (this alone is not proof).
2. Use a controlled endpoint and harmless metacharacter probes in a test environment or explicitly permitted target; avoid destructive commands, file writes, or outbound calls to third parties.
3. Confirm execution with a harmless, unique marker that cannot change state, and preserve the raw request/response evidence.
4. After confirmation, compare sibling features (webhook test, integration test, health check) for shared behavior using the same safe marker.
5. Stop after minimal proof; report each affected entry point and shared root cause without broad automation.
```

## Source

Intigriti Bug Bytes #240 (Sep 2026), citing researcher @saur1n, “A valid URL with a Command in its Shadow”: [https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-240-september-2026](https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-240-september-2026)

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
