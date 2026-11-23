---
description: Two-identity authorization differential scan for IDOR/BOLA — replay object URLs as a second account, compare against identity A and an anonymous control, emit LEAD-only results, and optionally run the deterministic verifier. Usage: /authz-diff --recon-dir recon/target.com --headers-a a.headers --headers-b b.headers --victim-marker a@example.com --scope target.com
---

# /authz-diff

Run the highest-value web2 test systematically: take requests identity **A**
legitimately made to its own objects, replay the exact same requests as identity
**B**, and add an anonymous control. Authz differential is how you prove BOLA/IDOR
without guessing object IDs — and how you avoid the classic "B just saw its own
data" false positive.

## Usage

```bash
# From an authenticated recon run (URLs A actually visited)
bughunter/tools/authz_diff.py \
  --recon-dir recon/target.com \
  --headers-a .private/a.headers \
  --headers-b .private/b.headers \
  --victim-marker alice@example.test \
  --attacker-marker bob@example.test \
  --scope target.com \
  --out findings/target.com/authz \
  --confirm

# From a HAR captured with /browser-capture
bughunter/tools/authz_diff.py \
  --har capture.har --headers-b .private/b.headers \
  --scope target.com --include-html
```

Agent path: the ReAct hunter calls `run_authz_diff` with `headers_a`,
`headers_b`, `victim_marker`, and optional `attacker_marker` (GET-only, scope
enforced by the dispatcher).

## Header files

Accepted formats: JSON object (`{"Cookie": "..."}`), Playwright storage-state
(`--storage-state-out` from `/browser-capture`), or `Name: value` lines.
Header values are never written to output; only header names are recorded.

## Verdicts

| Verdict | Meaning | Action |
|---|---|---|
| `CROSS_USER_MARKER` | B's response contains A's unique marker | Run `/validate`; deterministic IDOR verifier confirms |
| `PUBLIC_EXPOSURE` | A's marker is returned anonymously | Report as exposure, not identity differential |
| `IDENTICAL_ACROSS_IDENTITIES` | A and B get near-identical bodies on an object URL | Lead — inspect whether the object is shared or mis-scoped |
| `SAME_SCHEMA_DIFFERENT_DATA` | Same shape, different values for both identities | Medium lead — check ownership server-side |
| `DISTINCT_PER_USER` | Each identity sees its own marker | Negative control: isolation holds |
| `PUBLIC` | Anonymous control gets the same response | Not an access-control bug |
| `ENFORCED` | B is denied | No bug on this route |
| `UNKNOWN` | A baseline denied / transport error | Capture a request A legitimately owns |

## Safety rails

- Requires `--scope`; every URL is scope-checked before a socket opens.
- GET only; no object-ID guessing and no mutation of other users' data.
- Single-hop requests (no redirect following), response cap 64 KiB.
- Only marker-free lead metadata is persisted (URL, status, length, similarity).
- `--confirm` runs the existing IDOR oracle in memory; it does not auto-submit.

## Why not just Autorize?

Autorize (Burp) is excellent for interactive replay. This engine is the
headless, harness-driven equivalent: it ingests recon output or a HAR, filters
out-of-scope/static URLs, and uses schema-aware comparison plus marker controls
so the agent can run it without a human reading every diff. Similarity alone is
always a LEAD; only the cross-user marker oracle promotes to CONFIRMED.
