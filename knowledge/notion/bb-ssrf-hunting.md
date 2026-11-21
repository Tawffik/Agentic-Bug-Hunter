# SKILL: SSRF / Server-Side Request Forgery — HUNT-READY

**Skill id:** `bb/ssrf-hunting`  
**Source:** Notion Methodology OS — Module 10 (HUNT-READY)  
**Use with:** Universal Adaptive Hunting Methodology  

> **Authorized testing only.** LEAD until validated. Never auto-confirm. Prefer owned callback endpoints.

## When the agent should use this skill

- Target has URL fetch, webhook, preview, import, screenshot, PDF/render, or integration features
- Hunting track enters SSRF / server-side network capability
- Need structured experiments instead of payload spraying

## Execution directive

1. Locate the surface (feature, actor, object, trust boundary)
2. Build target model (what client sends, what server trusts, where decision is made, what consumes result)
3. Choose the security invariant (exact rule that must remain true — not a vuln name)
4. Establish legitimate baseline
5. Choose **ONE** controlled mutation
6. Run the smallest safe authorized test
7. Discriminate cheapest benign explanation first
8. Validate boundary crossing (unauthorized data/capability/state)
9. Measure smallest real impact, then chains only with evidence
10. Update model with positive and negative evidence
11. Stop/report when proven, disproven, unsafe, or no longer efficient

**If stuck:** WHERE AM I → SECURITY PROPERTY → BASELINE → ONE MUTATION → OBSERVE → DISCRIMINATE → VALIDATE → NEXT EXPERIMENT

## Required output contract

```
Target context → Security invariant → Hypothesis → Baseline → Mutation →
Observation → Discriminator → Validation → Impact → Negative knowledge → Next experiment
```

## Core mental model

```
Input → parser → validator → resolver → requester → network path → destination → response/side effect
```

SSRF is a **server-side capability problem**, not merely a URL parameter.

## Security invariants

- User-controlled destinations must not reach protected internal networks
- Validation must apply to the same canonical destination the requester contacts
- Redirect targets must be validated per policy
- DNS used for authorization must not silently change before connection (TOCTOU)
- Internal network position must not substitute for authentication
- Outbound requests must not inherit unexpected privileged context
- Nested/file parsers must not create hidden outbound requests that bypass outer validators

## Attack-surface discovery

Do not search only for parameters named `url`. Look for:

- Webhooks / callbacks / subscription verification
- Image, document, PDF, avatar, logo import
- URL preview / link scanner / screenshot / renderer
- Feeds, importers, repository/package fetchers
- Cloud/storage import, diagnostics, proxy/fetch endpoints
- REST/GraphQL arguments, async jobs and queues

Build: **User input → feature → worker/service → outbound client → destination**

## High-value research patterns

### Blind SSRF
Evidence ladder: DNS callback → HTTP callback → retry/redirect behavior → authorized internal target → demonstrated security effect.  
A callback proves interaction, **not** automatic access to sensitive internals.

### Validator / requester desync
Validator interprets destination X; requester contacts Y. Research hostname parsing, IPv4/IPv6 forms, encoding, userinfo, redirects, DNS timing, proxy vs direct resolution.

### Redirect methodology
Does policy apply to **every** hop in the redirect chain?

### DNS rebinding / TOCTOU
Validate at T1, connect at T2. Require reproducible difference between security decision and actual destination.

### Magic DNS / filter string vs resolved IP
Filters that block literal metadata/localhost strings but accept hostnames that resolve to them (e.g. nip.io / xip.io style). Confirm with real markers, not status alone.

### Inner-parser SSRF
Outer validator approves a file; downstream parser fetches another URL (PDF, SVG, fonts, media).

### Webhook / callback SSRF
Map: create → verify → test event → delivery → retries → redirects → headers → auth → update/delete.

### Cloud metadata
Treat as destination class. Impact from **demonstrated capabilities**, not the phrase metadata access.

### Internal services
After SSRF proof: reachable → authenticated? → readable? → writable? → privileged action?  
Do not collapse port reachability into compromise.

## Differential testing matrix (pick one dimension at a time)

| Dimension | A | B | Question |
|-----------|---|---|----------|
| Host form | canonical | alternate representation | same security decision? |
| IP family | IPv4 | IPv6 | same normalization? |
| Redirect | none | redirect | revalidated? |
| DNS | stable | changing | TOCTOU? |
| Protocol | HTTP | HTTPS | policy parity? |
| Port | default | alternate | restriction consistent? |
| Parser | URL | nested file reference | hidden requester? |
| Execution | sync | async | same policy? |
| Identity | anonymous | authenticated | outbound context changes? |
| Destination | public | internal | boundary enforced? |

## False-positive gate

Do **not** report: URL param with no server-side request, client-only DNS, unrelated callbacks, open ports without meaningful access, metadata reachability without capability, theoretical chains without evidence.

**Strong rule:** SSRF signal ≠ SSRF vulnerability.  
**Reportable shape:** server-side interaction → boundary crossing → unauthorized access/capability/state → reproducible evidence.

## Negative evidence (record deliberately)

localhost blocked · private ranges blocked · metadata blocked · redirects revalidated · IPv6 normalized · DNS changes ineffective · nested parser disabled · internal service requires auth

## Agent-ready primitive

```
InputSource → ServerSideRequester → ParserChain → ValidationPolicy → ResolutionPolicy
→ DestinationClass → ProtocolCapabilities → Observation → SecurityBoundary
→ Capability → Impact → Evidence → NegativeEvidence → RootCause → ChainCandidates
```

## HUNT-READY checklist

- [ ] SSRF-capable feature identified
- [ ] Server-side requester confirmed
- [ ] Baseline captured
- [ ] Parser/validator/requester chain mapped
- [ ] DNS and redirect behavior understood
- [ ] IPv4/IPv6 and representation differentials considered
- [ ] Inner-parser paths considered
- [ ] Blind OOB method available
- [ ] Protocol capability identified
- [ ] Internal/cloud destination classes considered
- [ ] Differential experiment performed
- [ ] Negative evidence recorded
- [ ] Real capability demonstrated
- [ ] Impact separated from theoretical chain
- [ ] Report evidence reproducible

## Permanent principle

SSRF hunting is **not** find a URL parameter and hit localhost.

It is: map server-side network capability → identify validation/resolution/requester boundaries → find interpretation or trust mismatches → design discriminating experiments → prove destination and capability → validate real impact → generalize root cause.

---
_Synced from Notion Bug Bounty Methodology OS · agent skill ready · authorized research only._
