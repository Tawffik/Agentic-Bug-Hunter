# SKILL: 🔔 Bug Bounty Tip — Subscription/Entitlement Checks Are Often Weaker Than UI Checks

**Skill id:** `tip/bug-bounty-tip-subscriptionentitlement-checks-are-often-weaker-than-ui-checks`  
**Category:** Auth Bypass, API Hacking, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e5dac31e88081d7bd63ff6244d6ddd4  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Type: Bug Pattern
Use when: the target has paid plans, premium features, quotas, exports, admin tools, or feature flags.

Where to look → Upgrade/downgrade flows, entitlement APIs, export/download endpoints, premium-only mutations, plan/role fields, and server responses after a trial or cancellation.

What to test → Compare the same action before and after a plan change using accounts you control. Inspect whether the client merely hides the feature while the backend still accepts the request. Test server-side enforcement on the final action, not only the pricing page.

Primitive / bypass → Business-logic or authorization failure where entitlement is enforced in the UI, a stale session, or a client-controlled parameter instead of on the server.

Validation / impact → Use a non-destructive premium feature or a test environment. Verify whether the server returns the protected result/action without a valid entitlement. Avoid consuming paid resources or bypassing real billing.

## Payload / Code

```
Look for plan, tier, subscription, entitlement, feature\_flag, quota, or role values in requests/responses; validate only with your own accounts.
```

## Source

[https://www.bugbountydirectory.com/blogs/subscription-bypass-leading-to-full-access-to-paid-features](https://www.bugbountydirectory.com/blogs/subscription-bypass-leading-to-full-access-to-paid-features)

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
