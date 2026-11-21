# SKILL: Next.js Middleware / Proxy — dynamic route parameter injection can bypass path checks

**Skill id:** `tip/nextjs-middleware-proxy-dynamic-route-parameter-injection-can-bypass-path-checks`  
**Category:** Auth Bypass, API Hacking, Fuzzing  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/408dac31e88081c79c2ae864222a2724  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Auth Bypass, API Hacking, Fuzzing**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

In affected Next.js versions, specially crafted query parameters could alter a dynamic route parameter as interpreted by the page while the visible URL path remained unchanged. Applications relying only on Middleware/Proxy path matching to protect dynamic routes could therefore render protected content without the expected check. The advisory applies to affected versions and route configurations, not every Next.js deployment.

## Payload / Code

```
In an authorized test app with a dummy protected dynamic route, compare the middleware's route/parameter interpretation with the page's final parameter and its own authorization decision. Change only the query parameter representation and verify whether the page independently enforces access. Use test data and confirm impact through the application's authorization behavior. Affected ranges listed by the advisory: Next.js 15.4.x before 15.5.16 and 16.0.x before 16.2.5; upgrade to a fixed release.
```

## Source

Official Next.js Advisory GHSA-492v-c6pp-mqqv / CVE-2026-44574: [https://github.com/vercel/next.js/security/advisories/GHSA-492v-c6pp-mqqv](https://github.com/vercel/next.js/security/advisories/GHSA-492v-c6pp-mqqv)

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
