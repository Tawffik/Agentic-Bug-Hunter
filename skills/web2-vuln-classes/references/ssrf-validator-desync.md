# SSRF — Validator / Requester Desync & Evidence Ladder

> SSRF is a **server-side capability problem**, not a URL parameter. The bug is that the destination the
> validator approved is not the destination the requester contacted, or that an inner parser made a
> request the outer validator never saw.

Use on in-scope targets with an approved callback endpoint. Prefer your own `interactsh-server` domain
(public `oast.pro`/`oastify.com` may be blocklisted). Never exfiltrate real data; prove reachability and
capability with a harmless marker.

---

## 1. Model the chain

```
user input -> parser -> validator -> resolver -> requester -> network path -> destination -> response/side effect
                                                      |
                                              inner parser (PDF/SVG/fonts/media)
```

For each feature record: who supplies the URL, what validates it, what resolves DNS, what client makes
the request, whether redirects are followed, and what the result does (render, store, display, ignore).

Security invariants:

- A user-controlled destination must not reach protected internal networks.
- Validation must apply to the **same canonical destination** the requester contacts.
- Every redirect hop must be revalidated.
- DNS used for authorization must not change before connection (TOCTOU).
- Internal network position must not substitute for authentication.
- Outbound requests must not inherit unexpected privileged context.
- Nested parsers must not create hidden outbound requests.

---

## 2. Where to look (not just `?url=`)

- Webhooks, callbacks, subscription verification, integration test buttons
- Image/avatar/logo/document/PDF import, URL preview, link scanner, screenshot/render
- Feeds, importers, package/repository fetchers, cloud storage import
- REST/GraphQL arguments, async jobs/queues, admin diagnostics, proxy/fetch endpoints
- PDF/headless-browser rendering of user HTML (invoice, report, export)
- SSO/metadata fetch, "connect your account" flows

Build: `user input -> feature -> worker/service -> outbound client -> destination`.

---

## 3. High-value desync patterns

### 3.1 Magic DNS (filter checks the string, not the resolved IP)

```
http://169.254.169.254.nip.io/latest/meta-data/
http://169.254.169.254.xip.io/latest/meta-data/
http://127.0.0.1.nip.io/
http://localtest.me/
```

If the literal IP is blocked but a hostname resolving to it is accepted, the validator is string-matching.
Confirm with real metadata markers in the body, not status alone.

### 3.2 Alternate loopback representations

```
http://127.1
http://127.0.0.0
http://2130706433        (decimal)
http://0177.1           (octal)
http://0x7f.1           (hex)
http://127.000.000.1
http://[::1]
http://[::]
http://localhost.
```

### 3.3 Redirect / hop handling

- Does the policy apply to **every** hop? Test `302 -> internal`, `302 -> metadata`, `307` preserving method/body.
- Does the HTTP client forward `Authorization`, `Cookie`, `Proxy-Authorization` or custom API-key headers
  across a cross-origin redirect? Use origin A (you control) -> 302 -> origin B (you control); inspect B.
  This is a server-side header leak, distinct from browser Referer leakage.
- Test same-origin vs cross-origin, HTTP vs HTTPS downgrade, and port changes.

### 3.4 DNS rebinding / TOCTOU

Validate at T1, connect at T2. Use a short-TTL domain you control that alternates between a public IP and
an internal one. Require a reproducible difference between the security decision and the actual destination.

### 3.5 Inner-parser SSRF

Outer validator approves a file; a downstream parser fetches another URL:

- PDF with remote images/fonts/annotations
- SVG with external `xlink:href` / `<image>`
- HTML-to-PDF / headless Chrome (img, iframe, script, fetch)
- Media/metadata parsers, office docs, ZIP/HTML wrappers

Test by embedding a callback URL in the rendered document and watching for a DNS/HTTP hit.

### 3.6 Webhook lifecycle

Map: create -> verify -> test event -> delivery -> retry -> redirect -> headers -> auth -> update/delete.
A verify step may be protected while delivery/test/retry is not.

### 3.7 Cloud metadata

Treat metadata as a destination class, not a finding. Impact comes from demonstrated capabilities:
`/latest/meta-data/iam/security-credentials/` (AWS), `metadata.google.internal` (GCP),
`169.254.169.254/metadata/identity/oauth2/token` (Azure). Prove the credential/token is usable only within
the program's rules; otherwise report reachability + data returned, redacted.

### 3.8 Internal services

After SSRF proof: reachable -> authenticated? -> readable? -> writable? -> privileged action?
Port reachability is not compromise. A 200 from an internal admin panel is a lead; reading data is the finding.

---

## 4. Differential matrix (one dimension at a time)

| Dimension | A | B | Question |
|---|---|---|---|
| Host form | canonical | alternate representation | same security decision? |
| IP family | IPv4 | IPv6 | same normalization? |
| Redirect | none | 1+ hops | revalidated per hop? |
| DNS | stable | changing | TOCTOU? |
| Protocol | HTTP | HTTPS | policy parity? |
| Port | default | alternate | restriction consistent? |
| Parser | URL | nested file reference | hidden requester? |
| Execution | sync | async | same policy? |
| Identity | anonymous | authenticated | outbound context changes? |
| Destination | public | internal | boundary enforced? |
| Header | none | custom auth | stripped across redirect? |

---

## 5. Evidence ladder

```
L0  Parameter looks like a URL                     -> not a finding
L1  DNS callback only                              -> blind interaction, not access
L2  HTTP callback with expected path/method        -> server-side request confirmed
L3  Callback proves a specific parser/redirect     -> chain understanding
L4  Response data from an internal/metadata source -> boundary crossing
L5  Demonstrated capability (credential usable, internal data read, action performed) -> reportable
```

Stop at the minimum level that proves impact. Record the callback timestamps and unique markers.

---

## 6. False-positive gate

Not reportable:

- A URL parameter with no server-side request.
- Client-side DNS/preflight only.
- An unrelated callback from your own browser/extension.
- Open internal ports with no meaningful access.
- Metadata reachability with no usable capability and no sensitive data.
- Theoretical chains without evidence ("could reach IAM -> could be RCE").
- A 200 from a generic internal page that requires auth for any real action.

Reportable shape:
`server-side interaction -> boundary crossing -> unauthorized data/capability/state -> reproducible evidence`

---

## 7. Negative evidence

Record deliberately: localhost blocked · private ranges blocked · metadata blocked · redirects revalidated ·
IPv6 normalized · DNS changes ineffective · nested parser disabled · internal service requires auth ·
content type rejected · outbound client strips auth headers.

## 8. Cross-links

- `skills/web2-vuln-classes/SKILL.md` (SSRF class + bypass tables)
- `skills/omni-killchain/references/ssrf-killchain.md`
- `bughunter/tools/oob_listener.py` / `/oob` for interactsh correlation
- `skills/cloud-pentest/SKILL.md` for post-access credential impact
- `skills/web2-exposure/SKILL.md` when the SSRF returns a config/secret artifact