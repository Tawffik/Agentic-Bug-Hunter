# SKILL: Information Disclosure / Exposure / Historical Intelligence — HUNT-READY

**Skill id:** `bb/info-disclosure`  
**Source:** Notion Methodology OS — Module 24 (HUNT-READY)  
**Use with:** Universal Adaptive Hunting Methodology, Recon/Exposure skill  

> **Authorized testing only.** A hostname, version, source map, error, or secret-looking string is a **SIGNAL** first — not automatically a vulnerability.

## When the agent should use this skill

- Live responses, JS, errors, exports, storage, or historical archives show unexpected data
- Need to classify exposure vs security boundary crossing
- Historical/Wayback candidates need current validation

## Execution directive

Same Universal loop:

1. Locate surface → 2. Target model → 3. Security invariant → 4. Baseline  
5. **ONE** mutation → 6. Experiment → 7. Discriminate → 8. Validate boundary  
9. Measure impact → 10. Update model → 11. Stop/report

**Required output:**  
`Target context → Security invariant → Hypothesis → Baseline → Mutation → Observation → Discriminator → Validation → Impact → Negative knowledge → Next experiment`

## Core mental model

```
Asset → Expected Visibility → Exposure Channel → Attacker Capability
→ Sensitivity → Security Boundary → Validation → Impact
```

For every observation ask:

1. What is the information?
2. Who should know it?
3. Who can obtain it now?
4. Through which channel?
5. Is the channel intended?
6. Is it actually sensitive?
7. Does access cross auth / privacy / tenant / trust boundary?
8. Can it enable another capability?
9. Can the consequence be proved safely?

## Information classification

| Class | Examples | Note |
|-------|----------|------|
| A — Public / expected | docs, public certs, intentional IDs | usually not a finding |
| B — Internal / contextual | internal hostnames, env names, feature flags | signal for model |
| C — Sensitive | private user/business data, protected config | boundary check required |
| D — Security-critical | active auth material, privileged credentials | capability validation |

Classification ≠ exploitability.

## Disclosure surface map

- **Live app:** HTML, headers, cookies, API/GraphQL/WS, errors, redirects, downloads, exports
- **Client artifacts:** JS bundles, source maps, manifests, service workers, mobile packages
- **Ops:** health, metrics, pprof, diagnostics, admin, stack traces, logs
- **Historical:** Wayback, Common Crawl, URLScan, old JS/APIs/docs, removed endpoints
- **External:** search engines, public repos, registries, issue trackers, object storage
- **Delivery:** CDN/cache/proxy, email, notifications, analytics, third-party integrations

## Priority scenario families

### Client-side / JS intelligence
Treat JS as application map: endpoints, roles, object names, GraphQL ops, internal domains, admin routes, legacy routes, debug code, env names, WS paths, undocumented params.

**Discovered endpoint = discovery signal.** Finding only after security property validated.

### Source maps
Exist ≠ vulnerability. Ask what security-relevant information they reveal beyond the intended production artifact.

### Secrets in client artifacts
Pattern match → classify → determine **capability** → scope → minimum-impact validation.  
Public client identifier ≠ private credential.

### Error / exception disclosure
Compare: valid → malformed → wrong type → missing/unexpected field.  
Learn which security-relevant information becomes observable — not make it error.

### Debug / metrics / pprof / actuator
Classify: metadata-only → architecture → sensitive data → privileged capability.

### Historical intelligence (high priority)
Scenario classes include: removed-but-still-live endpoint, old API version, old JS/map, deprecated admin route, removed parameter still accepted, historical subdomain/path with different auth, historical artifact revealing current architecture.

**Historical discovery generates candidates. Current validation decides whether a security issue exists.**

### 404 → information pivot
404 can still yield route-family clues, framework signatures, normalization, redirects, cache behavior, historical references.  
A 404 alone is not a vulnerability.

### Cross-user / cross-tenant
Actor A baseline → Actor B same operation → compare ownership/tenant/role on objects, exports, search, notifications, history, GraphQL nested fields, WS events.

### API / GraphQL field-level
Schema, object, field, error, and representation levels. Hidden fields, nested sensitive data, resolver auth gaps.

### Alternate representation
Same resource via HTML / JSON / CSV / PDF / mobile / GraphQL / download / debug — does every representation enforce the same visibility rule?

### CDN / cache / proxy
Context A response → cache → Context B receives it. Broken information boundary, not caching exists.

## Negative knowledge (explicitly not enough)

- Public API identifier alone
- Source map with no additional sensitive information
- Internal hostname alone
- Framework version alone
- Generic stack trace with no security consequence
- Public user ID / already-public data
- Dead historical endpoint with no current access
- Secret-looking string with no proven capability

## Agent-ready primitive

```
Observation → Channel → Classification(A–D) → Expected Visibility
→ Boundary Hypothesis → Controlled Comparison → Capability Proof
→ Impact → Negative Evidence → Graph Update
```

## HUNT-READY gate

Agent can: classify observations, separate signal from finding, use historical as overlay not proof, validate current accessibility, compare controlled identities, prove boundary crossing, record negative evidence, and hand off only validated LEADs to report template.

## Permanent principle

Do not hunt for extra data. Hunt for a **broken visibility invariant** with reproducible evidence.

---
_Synced from Notion Bug Bounty Methodology OS · agent skill ready · authorized research only._
