# Evidence Discipline — CONFIRMED vs NOT EXECUTED

> Credibility is lost faster by overclaiming one step than by reporting a smaller, proved impact.
> Separate what you **ran** from what you **inferred** on every multi-step report.

---

## 1. The chain table (mandatory for multi-step findings)

| Step | Action | Evidence | Status |
|---|---|---|---|
| 1 | Create attacker account A, victim account B | account IDs, timestamps | CONFIRMED |
| 2 | A reads B's object with A's session | raw request + response body showing B's data | CONFIRMED |
| 3 | A enumerates adjacent IDs at scale | 3 sample IDs + count, redacted | NOT EXECUTED (rate-limit policy) |
| 4 | Escalate to write/ATO | — | NOT EXECUTED (requires consent) |

Rules:

- Every step gets `CONFIRMED`, `NOT EXECUTED (reason)`, `FAILED`, or `BLOCKED`.
- `CONFIRMED` means you have the request/response or a reproducible observation.
- `NOT EXECUTED` is honest and acceptable; vague "could" language is not.
- Do not merge two different tests into one evidence screenshot.
- Severity is set by the **confirmed** steps. Describe the unexecuted ceiling separately.

## 2. Evidence quality ladder

| Level | Evidence | Report use |
|---|---|---|
| E0 | "The endpoint looks vulnerable" | not evidence |
| E1 | Status-code difference only | lead; not a finding |
| E2 | Response body differs, same identity | needs discriminator |
| E3 | Foreign object/data returned to an owned account | boundary crossing |
| E4 | Reproducible from clean session + negative control | CONFIRMED |
| E5 | Quantified impact (count/PII category/secret capability/state change) | severity basis |

## 3. Negative controls

Always include at least one:

- A sibling request that **should** be denied (and is).
- The same request with your own object (allowed).
- The same request unauthenticated (denied).
- A public resource that is expected to be public.

Negative controls prove the difference is authorization, not caching, SPA behavior or a generic error.

## 4. Evidence hygiene

- Redact cookies, tokens, API keys, and third-party PII before pasting.
- Prefer text/curl over screenshots; screenshots only for UI-only state.
- Include exact build/version/date, account roles, and tenant context.
- Record the full URL, method, headers that matter, and body.
- Save artifacts under `findings/<program>-<class>/evidence/`.
- Do not download bulk data to prove a leak; one record + count metadata is enough.
- State the program's safe-harbor/scope basis when the asset is unusual.

## 5. Language rules

| Avoid | Use |
|---|---|
| "could potentially allow" | "allows" (if proved) / omit (if not) |
| "may expose" | "returned X in the response" |
| "an attacker with access could" | "account A, authenticated as role R, can" |
| "critical RCE" (when only SSRF callback) | "server-side request confirmed; internal access not proved" |
| "full account takeover" (when only email leak) | "email address disclosure; ATO chain not executed" |

## 6. Pre-submit evidence gate

- [ ] Each chain step labelled.
- [ ] Severity matches confirmed steps only.
- [ ] Negative control included.
- [ ] PoC re-run immediately before submission.
- [ ] Secrets/PII redacted.
- [ ] Exact asset in current scope.
- [ ] Reproduction does not depend on your browser state or a warm cache.
- [ ] Unexecuted steps stated plainly, with the reason.
- [ ] Remediation addresses the root cause of the confirmed step.