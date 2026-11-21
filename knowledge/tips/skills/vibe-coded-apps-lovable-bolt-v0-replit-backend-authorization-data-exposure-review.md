# SKILL: Vibe-Coded Apps (Lovable / Bolt / v0 / Replit) → Backend Authorization & Data Exposure Review

**Skill id:** `tip/vibe-coded-apps-lovable-bolt-v0-replit-backend-authorization-data-exposure-review`  
**Category:** Recon, API Hacking  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e8808149b110e727a6321ca7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Escape's published study analyzed 5,600 publicly accessible vibe-coded apps and reported 2,000+ vulnerabilities, 400+ exposed secrets and 175 PII exposures. A separate 2026 study of 1,072 Supabase-backed AI-built apps reported RLS/access-control failures at scale. High-signal areas include backend APIs discoverable from JS, Supabase/Firebase access rules, storage buckets, source maps, admin-only routes, and server-side authorization missing behind front-end-only controls. These are aggregate studies, not a guarantee of bounty acceptance.

## Payload / Code

```
Passive-first on in-scope targets: fingerprint the builder from public HTML/JS; inspect public client bundles for API base URLs and exposed configuration; distinguish public anon/client identifiers from privileged service-role or secret keys; map documented/discovered API routes; then verify access-control only with your own account and benign records. For Supabase/Firebase, do not read or modify strangers' data. Never use discovered credentials or enumerate sensitive tables; stop at the minimum proof and redact values.
```

## Source

[https://escape.tech/blog/methodology-how-we-discovered-vulnerabilities-apps-built-with-vibe-coding/](https://escape.tech/blog/methodology-how-we-discovered-vulnerabilities-apps-built-with-vibe-coding/) ; [https://www.symbioticsec.ai/blog/we-scanned-1-072-vibe-coded-apps-98-had-security-flaws](https://www.symbioticsec.ai/blog/we-scanned-1-072-vibe-coded-apps-98-had-security-flaws) ; [https://www.bugcrowd.com/blog/hacking-vibe-coded-apps/](https://www.bugcrowd.com/blog/hacking-vibe-coded-apps/) ; [https://supabase.com/docs/guides/database/postgres/row-level-security](https://supabase.com/docs/guides/database/postgres/row-level-security)

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
