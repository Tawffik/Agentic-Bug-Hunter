---
description: Analyze JavaScript bundles for endpoints, parameters, secrets, client-side sinks, and source maps. Usage: /js-analyze <file-or-dir> [--out DIR] [--json]
---

# /js-analyze

Deterministic, offline extraction from JS bundles — the capability behind
`jsmax`. Pure and testable: it never sends a request, so point it at any bundle
(or pipe one in).

```bash
# Analyze a directory of downloaded bundles and write artifacts:
python3 bughunter/tools/js_analyzer.py analyze ./jsmax_downloads --out recon/target.com/js --json

# Analyze a single file (or stdin):
python3 bughunter/tools/js_analyzer.py analyze app.js
curl -s https://target.com/app.js | python3 bughunter/tools/js_analyzer.py analyze -
```

Extracts, into `--out`:

| File | Contents |
|:---|:---|
| `endpoints.txt` | rooted app paths from string/template literals (query stripped, assets filtered) |
| `urls.txt` | absolute URLs found in the bundle |
| `params.txt` | query-parameter names |
| `potential_secrets.txt` | AWS/GCP/Stripe/Slack/GitHub/GitLab/Twilio/SendGrid/Discord/S3/Firebase keys, JWTs, private keys, generic assignments |
| `sinks.json` | client-sink counts (eval, innerHTML, postMessage, document.write, …) |
| `sourcemaps.txt` | `//# sourceMappingURL=` / `//# sourceURL=` refs |
| `analysis.json` | full structured result |

`recon_engine.sh` runs this automatically after downloading the top-50 JS
bundles, writing `recon/<target>/js/` — which `lead_board.py ingest` already
reads (`js/endpoints.txt`), so discovered endpoints flow into the lead board
with no extra wiring.

Secrets are **lead-only signals** — verify a key is live and in-scope before
reporting.
