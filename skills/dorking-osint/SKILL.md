---
name: dorking-osint
description: Advanced search-engine, code-search and internet-wide-scanning OSINT for attack-surface discovery — Google/Bing dorks, GitHub code/org dorks, Shodan/Censys pivots (SSL CN, expired certs, favicon hash, copyright strings), reverse DNS/IP, origin-IP discovery, cloud bucket naming, acquisition/reverse-whois expansion, public SaaS misconfigs, Google Alerts monitoring and scoped dork automation. Use when recon needs new assets or historical exposure beyond DNS enumeration, when hunting leaked secrets/open panels/exposed files, or when you want to find quieter programs and forgotten infrastructure. Every hit is a lead until validated on an in-scope asset.
---

# Dorking & OSINT

> Search engines index what your wordlist never guesses. The job is **discovery + attribution + scope
> validation**, not collecting URLs. A dork hit is a lead; a brand match is not authorization.

## When to use

- Subdomain/URL recon is saturated and you need new asset classes (forgotten hosts, buckets, panels).
- You want leaked files/secrets/configs indexed by Google/Bing/GitHub.
- You need infrastructure pivots: TLS certificate, favicon hash, copyright string, reverse IP/DNS.
- You are expanding an acquisition's footprint or looking for less-crowded programs.
- You need continuous monitoring (Google Alerts, new indexed exposure).

Do not run mass dorking against a target that is not in the program's scope. Passive search is still
"touching" the brand; verify the asset is owned/in-scope before active testing.

---

## Operating rules

1. **Scope first.** A result that mentions the brand is not necessarily target-owned. Confirm DNS/WHOIS/
   certificate ownership and the program's in-scope list before requesting it.
2. **Search is passive; the asset is not.** Opening an indexed file is active. Treat a third-party host or
   a shared SaaS tenant as out of scope unless listed.
3. **No credential use.** Never authenticate with a discovered key/token. Report capability, not access.
4. **No bulk PII download.** One redacted record + metadata is proof. Stop immediately if real user data appears.
5. **Deduplicate and attribute.** Keep the query, timestamp, result URL and why you believe it belongs to the target.
6. **Classify.** `A public/expected`, `B internal/context`, `C sensitive`, `D security-critical`.
   Hand C/D to `web2-exposure` for boundary validation.
7. **Domain vs org matters on GitHub.** `"target.com"` is a code-search term; `org:TargetCorp` is a
   namespace. Never use `org:target.com` for a DNS name.

Full dork corpus: [references/dork-corpus.md](references/dork-corpus.md).
Validate exposure hits with `web2-exposure`; extract JS/secrets with `jsmax`; buckets with `cloud-pentest`.

---

## Workflow

```
Define scope + brand tokens
  -> generate query families (engine-specific)
  -> run bounded queries / automation
  -> deduplicate + attribute ownership
  -> classify result (A/B/C/D)
  -> minimal, non-destructive verification on in-scope asset
  -> convert to hypothesis for the owning skill
  -> record negative evidence + monitoring alert
```

Automation already in the repo:

```bash
# Google/Bing-style dork URL generation (no scraping; opens/prints queries)
python3 scripts/dork_runner.py -d target.com -c all -o dorks.txt
python3 scripts/dork_runner.py -d target.com -c credentials
```

`dork_runner.py` is a query generator, not a validator. See its categories and extend them with the
families below when needed.

---

## Query families that pay

### Search engines

| Goal | Pattern |
|---|---|
| Env/config exposure | `site:target.com (ext:env OR inurl:.env) ("DB_PASSWORD" OR "AWS_SECRET_ACCESS_KEY" OR "SECRET_KEY")` |
| Backups/dumps | `site:target.com (ext:bak OR ext:old OR ext:backup OR ext:sql OR ext:zip OR ext:tar.gz)` |
| API maps | `site:target.com (inurl:swagger OR inurl:openapi OR inurl:api-docs OR inurl:graphql OR intitle:"Swagger UI")` |
| Directory listing | `site:target.com intitle:"index of" (backup OR config OR .env OR .git OR private)` |
| Errors | `site:target.com ("sql syntax" OR "stack trace" OR "undefined index" OR "unhandled exception")` |
| Internal docs/PII | `site:target.com (filetype:pdf OR filetype:xls OR filetype:csv) ("confidential" OR "internal use" OR "password")` |
| Staging/dev | `site:target.com (inurl:test OR inurl:dev OR inurl:staging OR inurl:qa OR inurl:demo)` |
| Open redirects | `site:target.com inurl:return_to`, `inurl:redirect=`, `inurl:next=`, `inurl:continue=` |
| Internal extensions | `site:chrome.google.com/webstore "CompanyName"`, `site:addons.mozilla.org "CompanyName"` |
| Quieter programs | `site:slack.com "Has a bug bounty program"` |

Bing-only pivot:

```
ip:TARGET_IP (filetype:env OR filetype:sql OR filetype:bak OR filetype:log OR "DB_PASSWORD")
```

### GitHub code search

Always AND the target term, and exclude localhost/test noise.

```
"target.com" password
"target.com" (api_key OR apikey OR secret OR token)
"target.com" (AKIA OR aws_secret_access_key OR AWS_ACCESS_KEY_ID)
"target.com" filename:.env
"target.com" filename:credentials
"target.com" (DB_PASSWORD OR DATABASE_URL OR MYSQL_PASSWORD)
"target.com" ("BEGIN RSA PRIVATE KEY" OR "BEGIN OPENSSH PRIVATE KEY")
"target.com" (ghp_ OR github_pat_ OR gho_ OR glpat-)
"target.com" (sk_live_ OR rk_live_)
"target.com" (sk-ant- OR OPENAI_API_KEY OR ANTHROPIC_API_KEY OR xoxb- OR xoxp-)
"target.com" (mongodb+srv:// OR postgres:// OR mysql://)
org:TargetCorp path:.github/workflows ("pull_request_target" OR "secrets: inherit" OR "permissions: write-all")
```

Prefer verified-secret tooling over raw grep: `trufflehog github --org=TargetCorp --only-verified`,
`gh search code`. Treat hits as leads; a token near the brand may belong to a customer or a fixture.

### Shodan / Censys pivots

```
ssl.cert.subject.CN:"target.com"                 # unknown hosts on a cert
ssl:"target.com"                                  # cert-bound assets
ssl.cert.expired:true hostname:"target.com"       # forgotten hosts
http.title:"Grafana" OR http.title:"Kibana"
"X-Jenkins" "Set-Cookie: JSESSIONID" http.title:"Dashboard"
http.favicon.hash:<mmh3-hash>                     # same product/company icon
http.html:"© CompanyName"                         # copyright string pivot
```

Notes:

- Favicon hash: `python3 -c 'import mmh3,base64;print(mmh3.hash(base64.encodebytes(open("favicon.ico","rb").read())))'` (or `httpx -favicon-mmh3`).
- Copyright pivot: use a distinctive string from the footer, not a generic "All rights reserved".
- Certificate pivots reveal hosts that never appear in DNS enumeration.
- Censys equivalent: `services.tls.certificates.leaf_data.subject.common_name:"target.com"`.

### Reverse DNS / reverse IP / origin IP

```
for ip in $(cat ips.txt); do dig -x "$ip" +short; done     # PTR
# passive DNS: SecurityTrails / ViewDNS / crt.sh / urlscan
# origin IP candidates: historical DNS, TLS cert history, SPF/MX, subdomains that bypass CDN
```

Validate ownership before direct-IP testing. A random IP serving the same favicon is not necessarily in scope.
Never use an origin-IP bypass to evade a program's WAF rules if the policy forbids it.

### Acquisition / company expansion

- Reverse WHOIS on the registrant email/org; passive DNS for shared infrastructure.
- Certificate SANs often include acquired brands.
- Search the parent/acquired brand names, product names, and old domains.
- Check the program's policy: acquired subsidiaries are sometimes explicitly out of scope.

---

## Attribution checklist (before any active request)

- [ ] Result host resolves to an IP/ASN plausibly owned by the target.
- [ ] Certificate CN/SAN or WHOIS/registrant supports ownership.
- [ ] Host appears in program scope, or is a documented first-party asset.
- [ ] If SaaS/shared tenant: the specific tenant is listed, not just the provider.
- [ ] No third-party user data would be accessed by the test.

If attribution fails, record it as an out-of-scope lead and move on.

---

## Monitoring

- Turn high-value dorks into **Google Alerts** (`as-it-happens` or daily) for long-running programs.
- Re-run GitHub code search for new org repos and committed `.env` files after releases.
- Track new certificate entries (`crt.sh`), new subdomains, and JS bundle changes (see `web2-recon`).
- Store the query, date and previous result count so "new" is actually new.

---

## Negative knowledge

- A result mentioning the brand from a customer/partner repo is not target exposure.
- A public client key (`pk_`, Firebase anon, Maps browser key) is expected; only capability matters.
- An indexed URL that now 404s is historical, not current.
- A panel login page is not an exposed panel.
- An open S3 bucket name that returns `AccessDenied` is not a finding.
- A certificate with the company name on a third-party CDN is not necessarily target-owned.

## Output contract

For each result emit:

```
query | engine | result_url | ownership_evidence | class (A-D) | current_status | next_test | scope_ok
```

Then route: `C/D + in-scope` -> `web2-exposure`; JS/secrets -> `jsmax`; bucket/cloud -> `cloud-pentest`;
CI/pipeline -> `cicd-security`; panel/service -> `omni-killchain/references/exposed-services.md`.