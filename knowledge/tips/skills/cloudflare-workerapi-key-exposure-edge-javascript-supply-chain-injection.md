# SKILL: Cloudflare Worker/API Key Exposure → Edge JavaScript Supply-Chain Injection

**Skill id:** `tip/cloudflare-workerapi-key-exposure-edge-javascript-supply-chain-injection`  
**Category:** Recon, API Hacking, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e3dac31e8808131aecddbe99ea1fa2c  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A September 2026 incident showed how a broad Cloudflare API key exposed in application source could be used to create Workers, routes, and DNS changes, allowing JavaScript to be modified at the edge without changing the origin. The hunting lesson is to treat exposed CDN/edge credentials and third-party script delivery as a chain: source/config leak → edge control-plane access → route or Worker modification → customer-facing script integrity impact. Study Tab: JS/config/source maps → search for CDN or edge-provider credentials and deployment references → edge control-plane abuse → validate scope, permissions, and harmless response-integrity differences. Use when: a target uses Cloudflare Workers, Pages, CDN-managed scripts, or embeds third-party JavaScript across many customer sites.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

BreachHistory / Brevo incident analysis — 14–15 Sep 2026 — [https://breachhistory.com/blog/brevo-cloudflare-clickfix-supply-chain-september-2026](https://breachhistory.com/blog/brevo-cloudflare-clickfix-supply-chain-september-2026)

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
