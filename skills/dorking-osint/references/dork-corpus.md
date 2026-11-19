# Dork Corpus

> Replace `target.com`, `TARGET_IP`, `TargetCorp`, `CompanyName`. Every result is a **lead**.
> Authorized, in-scope assets only. Never use discovered credentials.

---

## 1. Google / Bing — files, configs, backups

```text
site:target.com (ext:env OR inurl:.env) ("DB_PASSWORD" OR "AWS_SECRET_ACCESS_KEY" OR "SECRET_KEY" OR "APP_KEY")
site:target.com (ext:log OR ext:txt OR ext:conf OR ext:cnf OR ext:ini OR ext:sh OR ext:bak OR ext:backup OR ext:swp OR ext:old OR ext:~ OR ext:git OR ext:svn OR ext:htpasswd OR ext:htaccess OR ext:json OR ext:yaml OR ext:yml OR ext:pem OR ext:key)
site:target.com (filetype:sql OR ext:sql) ("INSERT INTO" OR "CREATE TABLE") (password OR email OR credit)
site:target.com intitle:"index of" (.env OR .git OR backup OR config OR admin OR private OR sql OR dump OR credentials)
site:target.com (wp-config.php OR "wp-config.php.bak" OR "wp-config.php~" OR config.php.bak OR configuration.php)
site:target.com ("BEGIN RSA PRIVATE KEY" OR "BEGIN PRIVATE KEY" OR "BEGIN OPENSSH PRIVATE KEY" OR "BEGIN CERTIFICATE")
site:target.com inurl:.git ("HEAD" OR "config" OR "index of")
site:target.com (ext:bak OR ext:old OR ext:backup OR ext:~ OR ext:swp) (password OR secret OR key OR db_)
```

Bing-only IP search (Google does not support `ip:`):

```text
ip:TARGET_IP (filetype:env OR filetype:sql OR filetype:bak OR filetype:log OR "DB_PASSWORD")
ip:TARGET_IP intitle:"index of"
```

---

## 2. API maps / docs / panels

```text
site:target.com (inurl:apidocs OR inurl:api-docs OR inurl:swagger OR inurl:api-explorer OR inurl:redoc OR inurl:openapi OR inurl:graphql OR intitle:"Swagger UI")
site:target.com (inurl:swagger OR inurl:openapi OR inurl:api-docs OR inurl:graphql) ("swagger" OR "openapi" OR "__schema")
site:target.com inurl:actuator
site:target.com inurl:phpinfo
site:target.com inurl:server-status
site:target.com inurl:elmah
site:target.com inurl:telescope
site:target.com inurl:_profiler
site:target.com inurl:admin
site:target.com inurl:/phpmyadmin
site:target.com inurl:/jenkins
site:target.com inurl:/grafana
site:target.com inurl:/kibana
site:target.com intitle:"admin panel" OR intitle:"control panel"
```

---

## 3. Errors / stack traces

```text
site:target.com ("sql syntax" OR "warning: mysql" OR "stack trace" OR "undefined index" OR "unhandled exception" OR "server error" OR "exception")
site:target.com ("Fatal error:" OR "NullPointerException" OR "Traceback (most recent call last)")
site:target.com ("DEBUG = True" OR "APP_DEBUG=true")
```

---

## 4. PII / confidential documents

```text
site:target.com (filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xls OR filetype:xlsx OR filetype:csv) (confidential OR "internal use" OR "not for public" OR "do not distribute" OR password OR secret)
site:target.com filetype:pdf "date of birth"
site:target.com filetype:pdf "national id"
site:target.com (filetype:csv OR filetype:xls) ("email" AND "phone")
site:target.com intitle:"index of" ("users.csv" OR "customers.csv" OR "employee")
```

Do not download bulk PII. Confirm sensitivity on one redacted record.

---

## 5. Environments / subdomains / redirects

```text
site:target.com (inurl:test OR inurl:dev OR inurl:staging OR inurl:sandbox OR inurl:debug OR inurl:temp OR inurl:internal OR inurl:demo OR inurl:qa)
site:*.target.com
site:*.target.com (inurl:login OR inurl:admin OR inurl:api OR inurl:staging)
site:target.com inurl:return_to
site:target.com inurl:redirect
site:target.com inurl:url=
site:target.com inurl:next=
```

Open-redirect parameter names worth fuzzing once a candidate is found:
`return, return_to, return_url, redirect, redirect_to, redirect_uri, url, next, goto, destination, continue, callback, rurl, dest, forward, return_path`.

---

## 6. Cloud / storage / edge

```text
site:s3.amazonaws.com "target.com"
site:storage.googleapis.com "target"
site:firebaseio.com "target"
site:blob.core.windows.net "target"
site:r2.dev "target"
site:target.com (inurl:s3.amazonaws.com OR inurl:storage.googleapis.com OR inurl:blob.core.windows.net)
```

Bucket-name guessing: `target`, `target-prod`, `target-backup`, `target-assets`, `target-static`,
`target-dev`, `target-uploads`, `target-logs`, plus region suffixes. Verify ownership before reading;
`AccessDenied` is not a finding.

---

## 7. GitHub code search

Domain-scoped (code term):

```text
"target.com" password
"target.com" (api_key OR apikey OR secret OR token)
"target.com" (AKIA OR aws_access_key_id OR aws_secret_access_key)
"target.com" filename:.env
"target.com" filename:credentials
"target.com" (DB_PASSWORD OR DATABASE_URL OR MYSQL_PASSWORD)
"target.com" ("BEGIN RSA PRIVATE KEY" OR "BEGIN OPENSSH PRIVATE KEY")
"target.com" (ghp_ OR github_pat_ OR gho_ OR glpat-)
"target.com" (sk_live_ OR rk_live_)
"target.com" (sk-ant- OR OPENAI_API_KEY OR ANTHROPIC_API_KEY OR xoxb- OR xoxp-)
"target.com" (mongodb+srv:// OR postgres:// OR postgresql:// OR mysql://)
"target.com" (filename:openapi.json OR filename:swagger.json OR filename:docker-compose.yml OR filename:kubeconfig)
```

Org-scoped (GitHub namespace only):

```text
org:TargetCorp filename:.env
org:TargetCorp path:.github/workflows ("pull_request_target" OR "secrets: inherit" OR "permissions: write-all")
org:TargetCorp filename:package-lock.json
org:TargetCorp "BEGIN PRIVATE KEY"
```

Co-occurrence dorks that catch config snippets generic org searches miss:

```text
"Token=" "CompanyName"
"token=" "CompanyName"
"api_key" "CompanyName"
"client_secret" "CompanyName"
```

Use `trufflehog github --org=TargetCorp --only-verified` and `gh search code` for volume. Verify secret
validity only within program rules; never authenticate to unrelated services.

---

## 8. Shodan / Censys pivots

```text
ssl.cert.subject.CN:"target.com"
ssl:"target.com"
ssl.cert.expired:true hostname:"target.com"
http.title:"Grafana" OR http.title:"Kibana"
"X-Jenkins" "Set-Cookie: JSESSIONID" http.title:"Dashboard"
http.favicon.hash:<hash>
http.html:"© CompanyName"
http.component:"Jenkins"
port:6379 product:Redis
port:27017 product:MongoDB
port:9200 product:Elasticsearch
```

Censys:

```text
services.tls.certificates.leaf_data.subject.common_name:"target.com"
services.tls.certificates.leaf_data.validity.end < now
services.http.response.html_title:"Grafana"
```

Compute favicon hash with `httpx -favicon-mmh3` or:

```python
import base64, mmh3
data = base64.encodebytes(open("favicon.ico", "rb").read())
print(mmh3.hash(data))
```

---

## 9. Infrastructure / ownership pivots

```text
# Reverse DNS (PTR) for known IPs
for ip in $(cat ips.txt); do dig -x "$ip" +short; done

# Certificate transparency
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u

# Alternative CT API
curl -s "https://crt.name/v1/search?apex=target.com"

# Historical DNS / passive DNS
# SecurityTrails, ViewDNS, urlscan.io, Common Crawl index

# Reverse WHOIS / acquisition expansion
# search registrant email/org; pivot on shared nameservers, MX, SPF includes, analytics IDs
```

Origin-IP candidates: historical A records before CDN onboarding, direct subdomains, mail/SPF hosts,
TLS cert history, and hosts resolving to a non-CDN ASN. Validate ownership; do not bypass CDN to evade
program rules.

---

## 10. Internal extensions / public SaaS

```text
site:chrome.google.com/webstore "CompanyName"
site:addons.mozilla.org "CompanyName"
site:github.com "CompanyName" (extension OR plugin)
```

Internal Chrome/Firefox extensions published by mistake often contain API keys, internal hostnames and
undocumented endpoints. Inspect the extension package source; never use its credentials.

SaaS misconfiguration probes (only on listed first-party tenants):

```text
https://<company>.freshservice.com/support/signup
https://<company>.atlassian.net/  (open signup?)
https://<company>.service-now.com/
https://<company>.azurewebsites.net/
https://dev.azure.com/<org>/_projects
```

Open registration is a lead; the finding is access to internal tickets/users/documents after signup.

---

## 11. Program discovery / monitoring

```text
site:slack.com "Has a bug bounty program"
site:target.com ext:env
site:target.com filetype:pdf "confidential"
site:target.com intitle:"index of"
```

- Create **Google Alerts** for the static high-value dorks above.
- Re-run after releases/deploys; newly indexed content is often new exposure.
- Store query + date + result count to distinguish new hits from old noise.

---

## 12. Verification before reporting

| Check | Pass condition |
|---|---|
| Ownership | DNS/cert/WHOIS/in-scope evidence links the asset to the target |
| Currency | Result is live now, or historical access is revalidated |
| Sensitivity | Class C/D (private data, credential, internal control), not public/example |
| Boundary | An auth/privacy/tenant boundary is crossed |
| Evidence | One minimal redacted request/response; no bulk download |
| Program rules | Asset and bug class are in scope; no forbidden technique |

Anything that fails a row stays a lead. See `skills/web2-exposure/SKILL.md` for the validation ladder.