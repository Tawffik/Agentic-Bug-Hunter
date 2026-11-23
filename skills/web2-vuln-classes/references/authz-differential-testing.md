# Authorization Differential Testing — two identities, one request

IDOR/BOLA pays because authorization is checked per object, per action, and often
per representation. The only reliable way to find it is a **controlled identity
differential**, not ID guessing.

## The invariant

For a request that returns a user-scoped object:

```
A (owner)     -> 200 + object data
B (attacker)  -> 200 + A's data        => broken authorization
anonymous     -> 401/403               => control: not a public resource
```

If B receives its **own** data, or the endpoint returns the same public content
to everyone, there is no bug. Both cases look like "200 OK" to a naive scanner.

## Workflow

1. **Capture A's legitimate traffic.** Log in as A, exercise every feature, and
   save URLs/HAR (Burp "Copy URLs", Caido export, `/browser-capture --har`).
   Only A-owned object URLs are valid test inputs.
2. **Prepare B.** A second account, same role, no elevated privileges. Export its
   session headers (cookie / bearer). Never use another real user's session.
3. **Run the differential** over object-bearing URLs only:
   `bughunter/tools/authz_diff.py --recon-dir ... --headers-a ... --headers-b ...`
4. **Read verdicts, not status codes.** `PUBLIC` and `DISTINCT_PER_USER` are
   negative controls. `ENFORCED` means B was denied. Leads are
   `IDENTICAL_ACROSS_IDENTITIES` / `SAME_SCHEMA_DIFFERENT_DATA`; only
   `CROSS_USER_MARKER` is confirmable.
5. **Confirm with the oracle.** Supply A's unique marker (email, account number,
   private filename). The IDOR verifier proves B received it while anonymous
   access is denied.

## FP traps and how to kill them

| Trap | Why it fires | Control |
|---|---|---|
| `/api/me` or dashboard | each user gets their own data; bodies are similar | provide both A and B markers; `DISTINCT_PER_USER` wins |
| Personalised public page | anon page differs but all users get same layout | anonymous control similarity ≥ 0.90 → `PUBLIC` |
| Shared/global object | both identities legitimately see the same object | check ownership semantics; still a lead, not a confirmed bug |
| SPA catch-all 200 | unknown routes return the app shell | HTML skipped by default; JSON schema check |
| Cache/CDN variance | nonces/timestamps change bodies | volatile keys normalised before similarity |
| CSRF/session rotation | identical request from B fails for auth reasons | B denied → `ENFORCED` |

## Variant matrix (run beyond the captured URL)

Once the basic differential holds, test the **same object** through every
representation and verb the app exposes:

- Methods: GET → POST/PUT/PATCH/DELETE (approval-gated; do not mutate third-party data)
- API versions: `/v2/orders/123` protected, `/v1/orders/123` not
- Representations: `.json`, `/export`, `/pdf`, `/download`, older preview endpoint
- Wrappers: `{"id": 123}` vs `{"user": {"id": 123}}` vs `{"ids": [123]}`
- GraphQL: `node(id:)`, mutations, aliases, fragments
- Artifacts: invoice PDF, email attachment, signed URL, webhook payload

## Evidence rules

- Two identities, A-owned object URL, B's response containing A's marker,
  anonymous denial. Save the raw request/response for A, B, and anon.
- Do not include other users' PII beyond the single marker needed to prove the
  cross-tenant read.
- Similarity without a marker is a lead, never "confirmed IDOR".
- If the endpoint is public, report exposure (if sensitive) — not authorization.
