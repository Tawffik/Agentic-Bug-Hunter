# Parser Differential & Routing Authorization Bypass

> The bug is not "403 bypass". The bug is **two components disagreeing about which resource is being
> addressed** — a gateway authorizes representation A while the router executes representation B.

Use only on in-scope assets. One mutation per request. A 200 is not proof; the protected content or the
state change is proof. Pair with `/bypass-403`, `bughunter/tools/bypass_403.sh`, `waf_encoder.py` and
`bughunter/tools/waf_response_analyzer.py`.

---

## 1. Model the two views

```
client request
  -> CDN / WAF          (view 1: normalize, match deny rules, cache key)
  -> reverse proxy      (view 2: path rewrite, route match)
  -> framework router   (view 3: decode, normalize, select handler)
  -> authorization mw   (view 4: which path/object did it think this was?)
  -> handler / ORM      (view 5: what actually executed?)
```

Write down, for each layer you can infer: the raw path, the decoded path, the normalized path, and the
selected handler. The exploit exists where two of those differ in a security-relevant way.

Security invariants to test:

- The path authorized is the path executed.
- The host/port validated is the host/port contacted.
- The method that was authorized is the method executed.
- The parameter value checked is the value used.
- The body seen by the policy engine is the body processed by the handler.

---

## 2. Mutation matrix

Apply one dimension at a time against a **known protected route** and a **negative control**.

| Dimension | Variants to try | What a difference may mean |
|---|---|---|
| Case | `/Admin`, `/ADMIN`, `/admin` | case-sensitive deny rule vs case-insensitive router |
| Duplicate slash | `//admin`, `/api//v1/user`, `///admin` | proxy collapse vs router match |
| Dot segments | `/./admin`, `/a/../admin`, `/admin/.` | normalization order |
| Semicolon | `/admin;/`, `/admin/..;/`, `/;/admin` | Tomcat/Spring path-parameter handling |
| Encoded slash | `%2f`, `%252f`, `%2F` | decode-once vs decode-twice |
| Encoded backslash | `%5c`, `%255c` | Windows/IIS normalization |
| Encoded dot | `%2e`, `%252e`, `%2e%2e` | traversal normalization |
| Trailing chars | `/admin/`, `/admin.json`, `/admin.css`, `/admin%20`, `/admin%09`, `/admin#` | extension/static routing rules |
| Null/control | `%00`, `%0d%0a`, overlong UTF-8 `%c0%ae` | parser truncation |
| Unicode/emoji | `⬅️/`, full-width slash, homoglyphs | application-specific normalization |
| Query extension | `?x=.js`, `?file=admin.js` | gateway classifies as static |
| Leading slash / request-target | `GET admin`, `GET //admin`, absolute-form URI | HTTP client/proxy disagreement |
| HTTP/2 :path | non-canonical `:path` (missing leading `/`) | gRPC/router deny mismatch |
| Method | GET→POST/PUT/PATCH/DELETE/HEAD/OPTIONS, `X-HTTP-Method-Override`, `_method=` | per-verb authz gap |
| Header override | `X-Original-URL`, `X-Rewrite-URL`, `X-Forwarded-Prefix` | proxy trusts client path |
| Duplicate parameters | `id=mine&id=victim`, `id[]=mine&id[]=victim` | first/last value mismatch |
| Duplicate JSON keys | `{"id":1,"id":2}` | auth reads first, handler reads last |
| Content type | JSON↔form↔multipart | parser/authorizer uses a different body |
| Body size | normal vs oversized | policy engine truncates/skips body |
| Port form | `:443`, `:00443`, `:000443` | validator vs requester port parse |
| Host form | trailing dot, IDN, userinfo, IPv6/IPv4 | allowlist normalization |

Severity multiplier: a **vertical** bypass (user reaches admin) or a **cross-tenant** read/write beats a
single static file.

---

## 3. Known framework/primitive patterns

These are patterns to test, not universal exploits. Check version and configuration first.

| Component | Primitive | Test shape |
|---|---|---|
| Quarkus path auth | encoded semicolon / slash / backslash difference between policy and handler | protected route + `%3B` / `%2F` / `%5C` variants |
| `@fastify/express` | router normalization vs middleware path (duplicate slash, semicolon) | canonical vs normalized protected route; did auth middleware run? |
| gRPC-Go | non-canonical HTTP/2 `:path` without leading slash, deny vs fallback allow | canonical vs non-canonical `:path`; which handler selected? |
| Next.js middleware/proxy | crafted query parameter changes dynamic route parameter used by page | same visible URL, compare middleware decision vs page authz |
| Moby/Docker AuthZ | oversized request body omitted before policy evaluation | same harmless op, normal vs boundary body; inspect plugin input |
| Tomcat/Spring | `;/` path parameters, `..;/` traversal | protected route + `..;/` chain |
| IIS | `%5c`, trailing dot/space, short names | protected path variants |
| `follow-redirects` | array-form headers or regex metacharacters in `sensitiveHeaders` evade stripping | controlled origin A→B, canary `Authorization`; inspect B |
| Angular HttpClient | URL parse discrepancy may attach XSRF header cross-origin | controlled same-origin vs cross-origin request |
| Azure App Gateway v2 | query value containing `.js` may change 403 behavior (unverified) | baseline vs `?x=.js`; check real content, not status |

Full advisory-derived list: [framework-advisory-patterns.md](framework-advisory-patterns.md).

---

## 4. Procedure

```
1. Pick a protected endpoint with a known negative control (403/401).
2. Capture baseline: status, length, content-type, body hash, redirect chain, headers.
3. Pick ONE mutation from the matrix.
4. Send it. Compare against baseline, not against "200 = win".
5. Determine which handler/resource actually ran (body marker, error text, response schema).
6. Try the reverse control: a public sibling should behave identically if the difference is noise.
7. Record confirmed non-exploitable variants (negative evidence) — they define the parser boundary.
8. Escalate: read -> write; single object -> range; vertical -> cross-tenant.
```

Do not spray hundreds of variants at a WAF. Pace requests, use a canary object, and stop once the
boundary is proven.

---

## 5. False-positive gate

Not a finding:

- Different status but the same login/block page body.
- 200 with a generic SPA shell or empty JSON.
- A redirect to the same protected login.
- A WAF challenge page with a different status.
- Cached response from an unauthenticated context.
- Path accepted but the handler still enforces object ownership.
- Same-role access that is intended (e.g. admin reading admin data).

Reportable shape:
`security layer decision != execution decision -> protected resource/state actually reached -> reproducible evidence`

---

## 6. Cross-links

- `/bypass-403` command and `bughunter/tools/bypass_403.sh` for the header/method battery.
- `bughunter/tools/waf_response_analyzer.py` to distinguish block pages from real content.
- `skills/web2-vuln-classes/references/framework-advisory-patterns.md` for CVE-derived probes.
- `skills/johnwick/references/bypass-403.md` and `authz-idor.md` for per-verb/per-object testing.
- `skills/web2-exposure/SKILL.md` when the bypass reveals a file rather than an object.