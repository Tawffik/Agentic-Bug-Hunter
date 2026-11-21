# SKILL: Supabase Auth Misconfiguration Chain → Email Auto-Confirm + User Metadata Role Escalation (\$1,800 Case)

**Skill id:** `tip/supabase-auth-misconfiguration-chain-email-auto-confirm-user-metadata-role-escalation-1800-case`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081299c8fc3d3c7671f5c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

The key weakness is trusting a user-editable field (Supabase user\_metadata) as proof that a user is an admin. Supabase's official Security Advisor explicitly flags RLS policies that reference user\_metadata because a user can change it. Email auto-confirm is a separate configuration detail; it is not automatically a vulnerability without an impact or policy requirement. The \$1,800 bounty is a researcher's own report and the target is redacted.

## Payload / Code

```
Only on an in-scope program and with a test account: check whether signup requires email verification; inspect whether the app derives privileges from user-editable metadata; use only your own account to determine whether role-like metadata is accepted and whether a server-side authorization check blocks privileged actions. Never attempt to promote yourself on a real production target, access other users' records, or change real business data. Use a local clone or explicitly authorized test tenant for any write/role-change proof.
```

## Source

[Researcher-reported \$1,800 case (payout not independently verified)](https://medium.com/%40cyberrado57/exploiting-supabase-misconfigurations-authentication-bypass-and-privilege-escalation-for-1-800-f20d02557e47) ; [Supabase Security Advisor: user\_metadata is user-editable](https://supabase.com/docs/guides/observability/advisors?lint=0015_rls_references_user_metadata) ; [Supabase RLS guide](https://supabase.com/docs/guides/database/postgres/row-level-security)

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
