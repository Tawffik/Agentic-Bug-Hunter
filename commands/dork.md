---
description: Generate and triage scoped dork/OSINT queries — Google/Bing file exposure, GitHub code/org dorks, Shodan/Censys favicon/cert/copyright pivots, reverse IP/DNS, cloud buckets, origin-IP and acquisition expansion. Wraps scripts/dork_runner.py and the dorking-osint skill; every hit is a lead until ownership + scope + boundary are validated. Usage: /dork target.com [--category credentials|cloud|github|origin|all]
---

# /dork

Search engines index what DNS enumeration misses. Find the asset, prove it belongs to the target, then
validate exposure with `/exposure`.

**Load skill**: `skills/dorking-osint/SKILL.md` (+ `references/dork-corpus.md`).

## Run this

```bash
# All query families (prints queries + generated search URLs; no scraping)
python3 scripts/dork_runner.py -d target.com -c all -o dorks.txt

# Focused families
python3 scripts/dork_runner.py -d target.com -c credentials
python3 scripts/dork_runner.py -d target.com -c cloud
python3 scripts/dork_runner.py -d target.com -c github
python3 scripts/dork_runner.py -d target.com -c origin
```

For volume on code search, prefer verified tooling:

```bash
trufflehog github --org=TargetCorp --only-verified
gh search code 'org:TargetCorp filename:.env'
```

## Attribution gate (before any active request)

Run the automated gate over your collected hits (GitHub/URLScan/CDX/Google
results as JSONL `{"url":..,"source":..,"snippet":..}`) — it scores host
relationship + noise and ranks leads:

```bash
python3 bughunter/tools/exposure_attribution.py attribute --target target.com -i hits.jsonl
python3 bughunter/tools/exposure_attribution.py attribute --target target.com -i hits.jsonl \
  --min-verdict LIKELY --json --out attributed.jsonl
python3 bughunter/tools/exposure_attribution.py classify --url https://target.com/.env
```

Verdicts: `TARGET` / `LIKELY` / `WEAK` / `NOISE` / `UNRELATED` (LEAD-only — not a finding).
The manual checklist below is the human backstop when the gate says `TARGET`/`LIKELY`:

- [ ] Result host resolves to a target-owned IP/ASN or certificate/WHOIS supports ownership.
- [ ] Asset is on the program's current in-scope list (or documented first-party).
- [ ] SaaS result: the specific tenant is in scope, not just the provider.
- [ ] Testing would not read third-party user data.

If attribution fails → record as out-of-scope lead; do not request it.

## Triage each hit

| Hit | Next |
|---|---|
| `.env`, config, backup, `.git`, directory listing | `/exposure <url>` → `web2-exposure` |
| Swagger/OpenAPI/GraphQL docs | `/graphql-audit` or `web2-vuln-classes` (API map) |
| JS/source map/secret | `jsmax` |
| S3/GCS/Azure/R2 bucket | `cloud-pentest` / `/cloud-recon` |
| Jenkins/Grafana/Elastic/MinIO/Consul/Vault panel | `omni-killchain/references/exposed-services.md` |
| Public CI/build log/Azure DevOps | `cicd-security` |
| Open redirect parameter (`return_to`, `next`, ...) | `web2-vuln-classes` (open redirect/OAuth chain) |
| New subdomain/host | `/recon` / `web2-recon` — validate and add to the lead board |

## Monitoring

- Convert static high-value dorks into **Google Alerts**.
- Re-run GitHub code search after releases; re-check JS bundles/source maps.
- Track new cert entries (`crt.sh`) and new hosts; store query + date + previous count.

## Kill signals

- Brand mention from a customer/partner repo, not the target.
- Publishable client key with no capability.
- Indexed URL now 404s and is historical only.
- Login page (not an exposed panel).
- Bucket returns `AccessDenied` (not a finding).
- Certificate on a shared CDN with no ownership evidence.