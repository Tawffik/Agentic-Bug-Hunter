# SKILL: 🔔 Bug Bounty Tip — Treat AI/Agent Findings as Hypotheses Until You Reproduce Impact

**Skill id:** `tip/bug-bounty-tip-treat-aiagent-findings-as-hypotheses-until-you-reproduce-impact`  
**Category:** General, API Hacking  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e5dac31e88081daa22bd5ce101344e0  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General, API Hacking**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Type: Validation
Use when: an AI scanner, agent, LLM, or automated workflow reports SSRF, prompt injection, auth bypass, or data exposure.

Where to look → The exact request/response pair, the claimed trust boundary, the tool or connector invoked, and the sensitive asset allegedly reached.

What to test → Re-run the smallest reproduction with controlled inputs and a harmless canary. Check whether the result is actually server-side, cross-tenant, or privileged rather than a model inference, reflected text, or false positive.

Primitive / bypass → Evidence-quality failure: an apparent finding lacks a demonstrated security boundary violation.

Validation / impact → Require a reproducible request, observable side effect, and clear impact. Keep positive and negative controls, record the environment, and stop once the claim is proved or disproved. This validation loop is especially important because recent security research emphasizes that discovery volume without verification creates triage noise.

## Payload / Code

```
Use a harmless canary URL/token and a negative control. Do not send secrets or probe third-party infrastructure.
```

## Source

[https://projectdiscovery.io/blog/everyone-is-finding-vulns-the-hard-part-is-proving-them](https://projectdiscovery.io/blog/everyone-is-finding-vulns-the-hard-part-is-proving-them)

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
