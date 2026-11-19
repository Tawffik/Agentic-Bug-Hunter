# Framework Advisory Patterns

> Advisories are **pattern sources**, not exploit instructions. Re-validate on the current in-scope
> target, check the version/configuration, and prove the security consequence. A framework/version
> banner alone is not a finding, and a published CVE does not mean the target is vulnerable.

Use this when fingerprinting reveals a framework, when a dependency version is exposed, or when a
security layer and an execution layer appear to disagree.

---

## 1. Reusable primitives

| Class | Primitive | Why it pays | Test shape |
|---|---|---|---|
| Path/normalization | policy sees path A, router executes path B | vertical auth bypass, file access | protected route + encoded semicolon/slash/backslash, duplicate slash, case |
| Request-target | non-canonical HTTP/2 `:path`, absolute-form URI | deny rules match canonical form only | canonical vs non-canonical path; inspect selected handler |
| Route parameter | query param changes the dynamic route parameter used by the page | middleware-only protection bypassed | same URL, altered query representation; page-level authz check |
| Header forwarding | sensitive header forwarded across redirect/host boundary | credential/token leak | controlled origin A→B, canary header; inspect B |
| Body truncation | policy evaluates request without full body | authz bypass on large/oversized requests | harmless op, normal vs boundary body |
| Read-vs-write authz | read permission authorizes token replacement/update | account/integration takeover | two owned accounts/credentials; compare view vs mutate |
| Identity binding | token valid but not bound to org/tenant/session | cross-tenant access | two test orgs/accounts; same token, target other org |
| URL parse differential | validator and requester parse host/port/path differently | SSRF, allowlist bypass | controlled endpoint; compare validator decision vs outbound destination |
| Header array/object form | iterator sees indices instead of names | credential stripping bypass | local two-origin redirect with canary header in both forms |
| Oversized/encoded payload | parser/decoder disagreement | WAF/auth bypass, RCE | one mutation at a time, harmless marker |
| Image/native parser | complex format reaches native library | RCE/DoS | authorized lab with harmless marker; map trust boundary |
| Dependency source | remote URL/lifecycle script in package manifest | CI secret theft | inspect manifest/lockfile/build logs; isolated test build |
| Edge control plane | exposed CDN/edge API key | script integrity/supply chain | verify permissions only; do not modify production |

---

## 2. Advisory-derived patterns

### Next.js — middleware/proxy dynamic-route parameter injection
- Primitive: a crafted query parameter alters the dynamic route parameter the page uses while the visible
  URL path is unchanged; apps that rely only on middleware/proxy path matching can render protected content.
- Test: authorized app with a dummy protected dynamic route. Compare middleware route/parameter view vs the
  page's final parameter and its own authorization decision.
- FP gate: applies to affected versions/route configs, not every Next.js app. A rendered page without an
  authz decision is not proof; show the protected data/action.

### Quarkus / Jakarta path-based authorization
- Primitive: encoded semicolon (`%3B`), encoded slash (`%2F`) or backslash (`%5C`) are normalized
  differently by the policy engine and the resource handler.
- Test: known protected route + one encoding at a time; compare policy decision, resolved route and content.
- FP gate: 200 alone is not proof; confirm protected content or state change.

### `@fastify/express` — router vs middleware normalization
- Primitive: router normalizes duplicate slashes/semicolons while path-scoped auth middleware receives the
  original representation, so middleware can be skipped when normalization options are enabled.
- Test: canonical protected route vs duplicate-slash/semicolon variants; record whether auth middleware ran.
- FP gate: depends on adapter version and active normalization options.

### gRPC-Go — non-canonical HTTP/2 `:path`
- Primitive: router accepts a `:path` without the required leading slash while path-based authorization
  interceptors evaluate the non-canonical path; a deny rule for the canonical path can fail when a
  fallback allow rule exists.
- Test: authorized test server; canonical vs non-canonical path for a harmless method; inspect handler and
  interceptor observations.
- FP gate: requires path-based authorization and a fallback allow policy; not a universal gRPC bypass.

### follow-redirects — header stripping bypass
- Primitive A: array-form headers (`[name, value, ...]`) make iteration see numeric indices, so
  cross-host stripping of `Authorization`/`Cookie`/`Proxy-Authorization` silently fails.
- Primitive B: `sensitiveHeaders` builds a regex without escaping some metacharacters, so a valid header
  name containing `^` or `|` may not be stripped.
- Test: local two-origin redirect with a harmless canary credential header; compare object-form vs
  array-form and the configured sensitive-header name.
- FP gate: only matters when the client crosses hosts/downgrades protocol; do not use real credentials.

### Moby / Docker AuthZ — oversized body omitted
- Primitive: an authorization plugin may evaluate a request without the body when a specially crafted
  oversized API request triggers the condition; body-dependent policy then allows something it would deny.
- Test: authorized Docker lab; same harmless API operation with normal vs boundary body; log what the
  plugin receives and decides.
- FP gate: affects deployments using body-inspecting AuthZ plugins; not a generic Docker API bypass.

### n8n — credential read vs update, OAuth callback binding
- Primitive A: reconnect endpoint authorized with `credential:read` instead of `credential:update`, so a
  read-only user can replace stored token material with their own external account token.
- Primitive B: OAuth callback completes without binding the browser session to the flow initiator, so the
  wrong user's tokens are stored under the initiator's identity.
- Test: authorized lab with shared dummy credential / two controlled accounts + dummy provider; compare
  view vs reconnect; verify callback session binding and stored provider identity.
- FP gate: do not touch shared production credentials or trick real users into consenting.

### Casdoor — token exchange organization binding
- Primitive: token exchange validates JWT signature but not that the token's user belongs to the target
  application's organization; a valid token from one org can cross the org boundary.
- Test: two test orgs/accounts; check both signature validity and org/tenant membership; record subject,
  issuer, organization, target app, resulting permissions.
- FP gate: requires the missing binding check and affected versions; do not replay real users' tokens.

### Angular HttpClient — XSRF header parse discrepancy
- Primitive: URL-parsing discrepancy can cause the XSRF header to be attached to a request that resolves
  cross-origin (incomplete fix lineage).
- Test: local affected version; controlled same-origin and cross-origin URLs with a dummy token; observe
  header attachment.
- FP gate: dummy token only; never collect real anti-CSRF tokens.

### PHP memory-corruption advisories (patch-aware triage)
- Primitive: memory corruption in a specific PHP branch may lead to RCE under certain runtime conditions.
- Test: fingerprint exact PHP version/runtime; check vendor fix level; do not run random exploits on
  production. Treat version as a prioritization signal, not proof.
- FP gate: technology fingerprint alone is not a vulnerability; program policy may forbid exploit PoCs.

### HEIF/HEIC / native image parsers
- Primitive: a crafted image reaches a vulnerable native processing library; the higher-value escalation is
  the surrounding trust boundary (session/SSO/shared service).
- Test: authorized lab or program scope with a harmless marker; confirm parser crash/behavior, then map
  whether the processing service shares auth/session trust with higher-value systems.
- FP gate: a crash is not RCE; do not upload weaponized files to production.

### npm remote dependency URLs / install hooks
- Primitive: a package declares dependencies via attacker-controlled remote URLs or install-time scripts,
  moving execution outside the registry and into CI dependency resolution.
- Test: inspect `package.json`, lockfiles, lifecycle scripts, build logs, artifact metadata; use isolated
  test projects.
- FP gate: public package metadata is not a compromise; show execution or secret access.

### Cloudflare edge/API key exposure
- Primitive: an exposed CDN/edge API key can create Workers/routes/DNS changes, modifying JavaScript at
  the edge without touching origin.
- Test: determine the key's actual permissions with read-only calls inside program rules; map route/Worker
  control; do not modify production.
- FP gate: key presence alone is not impact; prove control-plane capability.

### Supabase / Firebase / Cognito client config
- Primitive: trusting user-editable metadata (`user_metadata`) for roles; open Realtime DB/Firestore rules;
  Identity Toolkit signup with unverified email; permissive Cognito identity pools.
- Test: own test account only; check whether server-side authorization derives privileges from
  user-editable fields; check read/write rules with a harmless key; do not read strangers' data.
- FP gate: a public anon key is expected; email auto-confirm is only a bug with a demonstrated impact.

---

## 3. Procedure

1. Fingerprint exact product/version from headers, JS, error pages, lockfiles, or exposed build metadata.
2. Read the advisory's **preconditions** (feature enabled, config shape, affected range).
3. Design the smallest controlled experiment on an in-scope host or lab.
4. Change one variable; keep a negative control.
5. Prove the security consequence (protected data/action), not just a status/error difference.
6. Record negative evidence and the exact version/config that made it non-exploitable.
7. Stop before destructive or production-impacting tests.

## 4. Reporting gate

- [ ] Version/config genuinely in the affected range.
- [ ] Preconditions present on the target, not assumed.
- [ ] Security consequence reproduced with evidence.
- [ ] No third-party data or persistent changes.
- [ ] Advisory/CVE referenced, but the report stands on your reproduction.
- [ ] Severity reflects proven capability, not the CVSS of the upstream CVE.