# SKILL: PHP URL Allowlist Edge Case: Zero-Padded Ports (<code>:000443</code>)

**Skill id:** `tip/php-url-allowlist-edge-case-zero-padded-ports-code000443code`  
**Category:** WAF Bypass, SSRF, Fuzzing  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e880812aaaebc88fcd9949b4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, SSRF, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A concrete parser-differential probe for applications that validate URLs with PHP parse\_url or a wrapper and then pass them to another URL parser/client. Some parsers normalize a zero-padded port such as :000443 to :443, while PHP parse\_url behavior can differ when the port contains more than five digits; the validator and the eventual requester may therefore disagree or error differently. This is a hypothesis probe, not a universal bypass. It matters only when the target has URL validation/fetching or a cache/routing decision tied to the parsed host/port.

## Payload / Code

```
In an authorized test, compare equivalent variants against a URL-validation endpoint or an app feature that fetches URLs:
- [https://controlled.example:443/](https://controlled.example:443/)
- [https://controlled.example:00443/](https://controlled.example:00443/)
- [https://controlled.example:000443/](https://controlled.example:000443/)

Record separately: validation result, normalized URL shown/stored by the app, actual outbound destination, and any cache/routing behavior. Use a domain and endpoint you control. Do not infer SSRF from a 200/500 response alone; prove the final destination or security decision changed. Stop if the feature would contact internal or third-party systems.
```

## Source

[https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits)

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
