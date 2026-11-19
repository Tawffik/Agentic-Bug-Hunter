---
name: web2-exposure
description: Information disclosure, exposure and historical-intelligence hunting — turns exposed files, debug surfaces, source maps, JS globals, archives, CI metadata and alternate representations into evidence-backed leads. Covers artifact families (.env/.git/backups/config/Actuator/Swagger/Source maps/Elmah/Laravel logs), Wayback/CDX/URLScan historical pivots, representation + artifact-equivalence + state-conditioned disclosure, deletion residue, invitation-state leakage and secrets capability validation. Use when a live response, JS bundle, error, export, storage or archive shows unexpected data and you need to decide whether it crosses a visibility boundary. Pairs with web2-recon, dorking-osint, jsmax and report-writing.
---

# Web2 Exposure & Information Disclosure

> Do not hunt for "extra data". Hunt for a **broken visibility invariant** with reproducible evidence.

A hostname, version, source map, stack trace or secret-looking string is a **SIGNAL** first.
`Exposure != Vulnerability`, `Discovery != Validation`, `200 OK != Finding`.

## When to use

- A live response, header, error, export, download, log, JS bundle or archive returns data the user did not expect.
- Recon produced a `.git`, `.env`, backup, Swagger, Actuator, phpinfo, source map or "index of" hit.
- Wayback/CDX/URLScan shows a removed path, old API or old JS that may still be live.
- You need to decide whether a leak is reportable or merely noise.
- A secret-like token was found and you must establish **capability** before reporting.

Do NOT use this skill to brute-force giant wordlists. Use the bounded catalog in
[references/artifact-catalog.md](references/artifact-catalog.md), and only on in-scope hosts.

---

## Core model

```
Asset -> Expected visibility -> Disclosure channel -> Who can obtain it now
      -> Sensitivity class -> Security boundary crossed -> Validation -> Impact
```

For every observation answer:

1. What exactly is the information?
2. Who should be allowed to know it?
3. Who can obtain it **now**, from which channel?
4. Is that channel intended?
5. Is it actually sensitive (not already public, not a placeholder)?
6. Does access cross an authentication, privacy, tenant or trust boundary?
7. Can it enable another capability (credential, session, internal route, write)?
8. Can the consequence be proved safely with minimal data?

If questions 1, 3, 5 and 6 are not all answerable, it is a **LEAD**, not a finding.

## Sensitivity classes

| Class | Examples | Treatment |
|---|---|---|
| A — public/expected | docs, public certs, publishable client keys, intentional IDs | usually not a finding |
| B — internal/contextual | internal hostnames, env names, feature flags, stack traces | signal for the target model |
| C — sensitive | private user/business data, protected config, PII | boundary check required |
| D — security-critical | live auth material, privileged credentials, session tokens | capability validation required |

Classification is not exploitability. A class-D string with no proven capability is still a lead.

---

## Execution directive

1. **Locate** the surface and capture the exact request/response (method, URL, auth context, headers, body hash).
2. **Model** the object: owner, tenant, intended audience, representations, lifecycle states.
3. **State the invariant**: "this artifact is only visible to X", "deleted means unreachable", "export and UI expose the same fields".
4. **Baseline** the legitimate/public view.
5. Apply **one** mutation (alternate representation, alternate state, alternate identity, historical copy, derived sibling path).
6. **Discriminate**: could this be public-by-design, a fixture, a stale cache, a generic error, a placeholder?
7. **Validate** an actual boundary crossing with an owned account/object.
8. **Quantify** the minimum real impact; stop before bulk extraction.
9. **Record negative knowledge** (what was correctly protected).
10. Hand validated leads to `report-writing`; hand hypotheses to the owning hunting skill.

Output line:
`context -> invariant -> baseline -> mutation -> observation -> discriminator -> validation -> impact -> negative evidence -> next experiment`

---

## Artifact families (high-signal first)

Full path catalog, content markers and validation ladders:
[references/artifact-catalog.md](references/artifact-catalog.md).

| Family | Examples | What makes it a finding |
|---|---|---|
| VCS metadata | `/.git/HEAD`, `/.git/config`, `/.svn/wc.db` | reconstruction yields source/secrets **and** is reachable now |
| Env/config | `/.env`, `config.php`, `appsettings.json`, `web.config`, `.npmrc` | live credentials/internal endpoints, not example values |
| Backups/dumps | `.zip/.tar.gz/.sql/.bak/~`, root-domain archives | real PII/source/credentials, not an empty template |
| API maps | OpenAPI/Swagger/GraphQL/`redoc` | unauthenticated routes or admin operations become testable |
| Diagnostics | `/actuator/env`, `/actuator/heapdump`, `phpinfo`, `elmah.axd`, `trace.axd`, Laravel logs, Symfony profiler | secrets/session cookies/env vars, not just a version banner |
| JS artifacts | source maps, bundles, `window.*` globals, postMessage handlers | hidden routes/secrets/handlers that change the attack surface |
| Storage | S3/GCS/Azure/R2/MinIO listings | unauth list/read of non-public objects |
| Historical | Wayback/CDX/URLScan/CommonCrawl | old endpoint/secret that is **still reachable or still valid** |
| CI metadata | public build logs, artifacts, pipeline YAML, Azure DevOps public projects | tokens/internal hosts/deployment graph |
| Alternate representations | `.json`, `?format=json`, Accept header, export/download/PDF/ZIP | fields or objects the primary view intentionally hides |

`Hidden` does not mean vulnerable. `Exposed` does not mean sensitive.

---

## Historical intelligence (highest-yield when live is patched)

```
known URL/path -> current status (404/403/410) -> Wayback/CDX/URLScan -> historical 200
-> extract paths, hosts, parameters, tokens, comments -> current revalidation -> boundary test
```

Rules:

- Keep **historical surface** separate from **current surface**. An archived 200 is not current access.
- Always revalidate current reachability before reporting.
- Use `web.archive.org/cdx/search/cdx?url=...&fl=original&collapse=urlkey` plus `waybackurls`, `gau`, URLScan.
- Look for removed APIs, old JS, deprecated admin routes, old parameters still accepted, historical subdomains with different auth.
- Archived copy alone is not a finding. The finding is *current* access to data that should not be current.

Query patterns and a triage checklist are in [references/artifact-catalog.md](references/artifact-catalog.md).

---

## Differential disclosure families

These four patterns pay disproportionately and are routinely missed by scanners.

### 1. Representation differential

Same object, different serializer:

```
/resource          (HTML)
/resource.json
/resource?format=json
Accept: application/json
/resource.xml
/resource/export
/resource/download
/resource.pdf
```

Compare status, content-type, key set, nested objects, metadata and authorization-sensitive fields.
A `.json` suffix or schema difference alone is not a bug; a **sensitive field outside intended visibility** is.

### 2. Artifact equivalence

The same data is reachable through several artifacts: page, API, export, download, PDF, ZIP, attachment, email, notification.
Collect each representation for the **same object** and compare ownership, authorization and fields.
The weak artifact is usually the export/download/attachment path.

### 3. State-conditioned disclosure

Authorization/serialization often differs by object state: `draft`, `preview`, `pending`, `archived`, `shared`, `deleted`, `expired`, `exported`.
Test the same owned object across states and compare visibility.
Do not perform destructive state changes on production data.

### 4. Deletion residue

Deletion from the primary surface does not guarantee deletion from secondary copies:
draft/preview, export, attachment, CDN/object URL, email/notification copy, API reference, search index.
Confirm the artifact still returns data that should be gone.

Also test **invitation-state leakage**: `invited/pending/accepted/expired/revoked` membership can expose
resource titles/metadata before authorization completes. Record the exact state and the exact field exposed.

---

## Secrets: pattern -> capability -> minimum proof

1. Extract candidate with provenance (file, URL, commit, timestamp).
2. Classify: public client identifier vs private credential vs placeholder/fixture.
3. Determine **capability**: which API, scope, tenant and account does it authenticate?
4. Prove the smallest capability on an authorized target with a read-only call. Never authenticate against
   unrelated services, never modify data, never exfiltrate.
5. Redact the value in every artifact and report. Report the capability, not the string.
6. If capability cannot be proven, it is at most a lead and often not reportable.

Public browser keys (Google Maps/Firebase/Supabase anon) require an **impact** check: which APIs are enabled,
which restrictions exist, and whether an unintended security action is possible. Key presence alone is Low/Info.

---

## 404 / 403 / redirect pivots

A negative status is a state to explain, not an end state:

- **404 subdomains**: probe backend error pages, stack traces, bucket paths, `/humans.txt`, config siblings.
- **403/401 hosts**: check archived snapshots, alternate methods, path normalization (see
  `skills/web2-vuln-classes/references/parser-differential-bypass.md`), and sibling hosts.
- **Redirecting root**: fuzz the original host/path instead of following the redirect; forgotten files often remain.
- **Empty API subdomain**: try the full Swagger/OpenAPI path family, not just `/`.
- **Different 404 fingerprint**: may indicate a separate backend/API context — treat as a lead, then map JS for the real API host.

---

## Evidence discipline

Record both positive and negative results. Negative knowledge is what stops false positives:

- localhost/private ranges blocked
- redirects revalidated
- source map with no additional sensitive info
- internal hostname with no reachable consequence
- generic stack trace with no security impact
- public user ID / already-public data
- dead historical endpoint with no current access
- secret-shaped string with no proven capability

Promotion gate:
`Observation -> boundary crossed -> invariant violated -> unauthorized capability/data/state -> reproducible evidence`

Only then is it `CONFIRMED`. Everything before is `LEAD`.

---

## Handoffs

| Situation | Next skill |
|---|---|
| Need more assets, JS, historical URLs | `web2-recon` |
| Need search-engine/GitHub/Shodan pivots | `dorking-osint` |
| Source map / bundle / secret extraction | `jsmax` |
| Bucket or cloud credential impact | `cloud-pentest` |
| Public CI / pipeline metadata | `cicd-security` |
| Chat widget / support transcript leak | `agentic-app-audit` (chat reference) |
| Authorization edge cases on the leaked object | `web2-vuln-classes` (authz) + `johnwick/references/authz-idor.md` |
| Validate and write | `triage-validation`, `report-writing` |

## Quick gate before reporting

- [ ] Artifact is on a **current** in-scope asset, reachable now.
- [ ] Exact request/response captured; no bulk data downloaded.
- [ ] Sensitivity class C/D, not A.
- [ ] A real auth/privacy/tenant boundary is crossed (not just "interesting data").
- [ ] Impact proved with an owned account or a documented business consequence.
- [ ] Negative controls recorded.
- [ ] Secret values redacted everywhere.