# Target Understanding → Best-Way Lifecycle (2026-11-23)

Built **before** hunting, from every signal the toolkit has (app-model, tech, params,
JS/spec extraction, lead boards). Content pages (docs/blog/marketing) are excluded
from the object/IDOR surface. This is the "understand all targets first, then pick
the best lifecycle path" gate.

| Target | Hosts | Endpoints | Object-ref eps | Leads | Tech | Real surface |
|---|---|---|---|---|---|---|
| tiktok.com | 41 | 9542 | 2781 (video/{id}) | 80 | Cloudflare, S3, Apache, Apple-Sign-in | huge, mature; signed APIs |
| temu.com | 37 | 2242 | 65 | 31 | Cloudflare, HSTS | large; api/upload/oauth |
| aiven.io | 133 | 1215 | 33 | 5 | Cloudflare, AWS | **3 SPA auth endpoints** + MCP/SAML |
| pipopay.com | 9 | 76 | 29 (cashier/checkout) | 10 | (edge) | payments, session-walled |
| volkis.com.au | 39 | 215 | 5 | 0 | Astro, Cloudflare | static marketing |
| soundon.global | 1 | 1 | 0 | 0 | — | negligible |

## Per-target understanding → best way

### tiktok.com — largest surface, extreme competition
- **Understanding:** 9542 endpoints; object refs are video content (`/@user/video/{id}`), not IDOR money. Real leads: `api-misconfig` 33, `http-smuggling` 10 (low), `file-upload` 9, `oauth` 7. Signed/`a_bogus` APIs; Cloudflare/Akamai edge.
- **Best way:** don't crawl the core. **Recover endpoints from APK/JS** (`client-reverse`, `jsmax`), then hit **regional/aux hosts** (`*-my`, `*-usp`, `*-sg`, `*-alisg`, `autofill-*`, `risk-*`) where duplicate risk is low; focus `api-misconfig` + `file-upload` + `oauth`. Needs auth for most. **Do not** bulk-scan (program rules).
- **Lifecycle path:** JS/APK endpoint recovery → auth (2 identities) → api-misconfig/upload → `/authz-diff` on object APIs.

### temu.com — large, auth-gated
- **Understanding:** 2242 endpoints; 31 leads (`api-misconfig` 15, `file-upload` 9, `oauth` 5, plus sqli/xss killed correctly).
- **Best way:** `api-misconfig` + `file-upload` + `oauth`; needs a session. Verify the 2 killed auto leads are truly dead (they were: timing/CSP).
- **Lifecycle path:** get a session → api-misconfig triage → upload abuse → authz diff.

### aiven.io — small real surface
- **Understanding:** 1215 endpoints but the real attack surface is **3 SPA auth endpoints** (`console.aiven.io/login`, `/oauth/authorize`, `/profile/auth`) + the MCP product page. Everything else is docs/blog (now filtered). Automation: 0 confirmed, 0 FP.
- **Best way:** **manual OAuth/MCP consent** testing (`mcp-server-audit`, `agentic-app-audit`) and the **SAML ACS** (one DNS TXT away). The two held MCP candidates (A/B, Medium) are the submittable value.
- **Lifecycle path:** unblock SAML DNS → XXE OOB path (already built) → duplicate-check A/B → submit Medium.

### pipopay.com — payments, session-walled
- **Understanding:** 9 hosts, 76 endpoints; object refs are cashier/checkout pages. Source-leak leads killed (edge 403, no secret). Session gate enforces `permission error` on user endpoints.
- **Best way:** **capture a real cashier session** (needs an in-scope TikTok product checkout) → test IDOR/amount/order tampering + stored-card IDOR via two identities.
- **Lifecycle path:** acquire session → `/authz-diff` on `pre_order_id`/`stored_method` → business-logic amount tampering.

### volkis.com.au — static, drop
- **Understanding:** Astro static marketing; 215 endpoints; 0 leads (was 100% noise before router fixes).
- **Best way:** passive only; low value. Do not spend active time unless a dynamic subdomain appears.

### soundon.global — dead
- 1 endpoint; drop.

## Best-way ranking (where to go deep first)
1. **pipopay** (payments, low dup) — *if* a cashier session can be obtained.
2. **tiktok regional/aux hosts** — largest low-dup surface; needs JS/APK recovery + auth.
3. **aiven** — SAML/MCP manual; one DNS action from testable; held Mediums.
4. **temu** — api/upload/oauth with a session.
5. Skip: volkis (static), soundon (dead).

## Rule
No target advances to the hunt lifecycle until this understanding is refreshed
(`app_model` + tech + params + leads). Automated hunts run only on the `auto`
lane; `authz`/`ai` lanes need identities/canaries — that is the real blocker,
not more scanning.