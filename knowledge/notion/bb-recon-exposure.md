# SKILL: Recon / Exposure / Attack Surface Discovery — HUNT-READY

**Skill id:** `bb/recon-exposure`  
**Source:** Notion Methodology OS — Module 17 (HUNT-READY)  
**Use with:** Universal Adaptive Hunting Methodology, Info Disclosure skill  

> **Authorized testing only.** Discovery ≠ Validation ≠ Security Impact.

## When the agent should use this skill

- Starting or expanding authorized engagement
- Need to turn observations into a security model, not a flat asset list
- Prioritizing what to test next

## Core model

```
Scope → Asset Model → Discovery → Validation → Correlation
→ Attack-Surface Graph → Signal → Hypothesis → Evidence → Next Test
```

## Core questions

- What is in scope?
- What assets and relationships exist?
- Which observations are current and owned by the target?
- Which observation changes the security model?
- Which trust boundary does it reveal?
- What is the smallest useful next experiment?
- What evidence proves the security consequence?

## Asset model (relationships, not flat lists)

```
Organization → Product → Domain → Subdomain → DNS → IP/ASN → Host
→ Technology → URL → JS → API → Object → Identity/Tenant → Cloud/Third Party
```

Preserve provenance, timestamps, confidence, and validation state.

## Discovery layers

**Passive:** CT logs, historical DNS, archives, search engines, public code/JS, URL indexes, public infrastructure references.

**Active (authorized):** DNS resolution, HTTP validation, service/content discovery, vhost validation, crawling, controlled interaction.

## Research loops

| Loop | Flow |
|------|------|
| Asset | Discovery → Resolution → Validation → Relationship |
| Application | Host → HTTP → Technology → Content → JS/API → Application Model |
| Security | Observation → Trust Boundary → Invariant → Hypothesis → Experiment → Evidence |
| Adaptive | New Evidence → Update Graph → Change Priority → Targeted Discovery → Validation |

## Domain / DNS / HTTP

- DNS: Discovery → Resolution → HTTP Validation → Ownership/Scope Classification
- HTTP baseline per live host: status, redirects, content type/size, headers, cookies, TLS, CDN/WAF, auth state, technology, fingerprint
- Treat 401/403/404/redirects/errors as **states requiring explanation**, not findings by themselves

## Application / API / JS

Build: **endpoint → method → parameter → object → identity → tenant → capability**

JS is vocabulary and relationship evidence: routes, methods, params, object IDs, roles, feature flags, API versions, WS, IdP, upload/download, source maps, integrations. Preserve provenance to source artifact.

## Historical surface

Keep **Historical Surface** separate from **Current Surface**. Historical evidence can reveal legacy APIs, forgotten apps, alternate hosts, old auth paths, storage references. **Always revalidate current reachability.**

## Hidden surface (candidates, not findings)

Staging, admin interfaces, alternate API versions, health/debug routes, upload/export processors, webhook handlers, legacy apps, alternate hostnames, forgotten mobile APIs.  
**Hidden does not mean vulnerable.**

## Correlation over enumeration

Ask: **What relationship did this observation create?**  
Example: certificate → hostname → DNS → host → app → JS → API → object identifier → authorization hypothesis.

## Confidence scale

```
UNVERIFIED → CANDIDATE → CORRELATED → VALIDATED → SECURITY-RELEVANT
```

Preserve negative evidence: historical-only, unrelated host, dead endpoint, revoked/placeholder value, stable blocked behavior, inaccessible storage.

## Recon → hypothesis

Every useful observation becomes one of:

1. **Discard**
2. **Enrich**
3. **Prioritize**
4. **Hypothesis**

Example: New API route → identify object ID → identity/tenant context → authorization hypothesis → controlled comparison.

## Prioritization

Prefer discoveries that expose or connect: new trust boundaries, privileged functions, object identifiers, tenant boundaries, auth states, legacy components, unusual parsers, management surfaces, cross-component relationships, strong provenance, or meaningful behavioral differences.

This is **research priority**, not vulnerability severity.

## Automation / CI boundary

```
Source → Collector → Normalizer → Resolver → Validator → Correlator → Graph → Prioritizer → Evidence
```

- **BugBountyCI / recon tools** = Discovery Producer (collect, normalize, package)
- **Security Research Agent** = Reasoning / Validation Engine (interpret, hypothesize, experiment, decide next)

Keep reasoning logic out of the recon producer.

## Agent-ready primitive

```
Pattern: new asset or relationship reveals an additional attack-surface node
Hypothesis: the node changes a reachable trust boundary or capability
Procedure: discover → validate → correlate → classify scope → attach to graph → identify boundary → targeted experiment
Evidence: verified asset + relationship + reachable capability + security consequence
Strategy: prefer discoveries that change the next decision and increase information gain
```

## HUNT-READY gate

Agent can establish scope, model assets/relationships, distinguish discovery from validation and ownership from technical association, separate historical from current, map HTTP/API/JS surfaces, correlate into a graph, convert signals into hypotheses, choose targeted experiments, preserve false positives and negative evidence, prove security consequence instead of exposure alone, and feed context into the next methodology.

## Final invariant

**Recon succeeds when it changes the security model of the target.**  
Enumeration without changing what you can reason about or test next is data accumulation, not research.

---
_Synced from Notion Bug Bounty Methodology OS · agent skill ready · authorized research only._
