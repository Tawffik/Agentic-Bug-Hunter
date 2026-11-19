# Exposure Artifact Catalog

> Bounded, high-signal candidates for **authorized** content discovery. This is not a brute-force
> wordlist. Always apply `scope_checker`, a low rate limit, and a `LEAD`-only classification.
> `200` alone is never proof — inspect content-type, body markers and authorization context.

---

## 1. Path families

### VCS / source reconstruction

```
/.git/HEAD                 -> "ref: refs/heads/" (plain text, not HTML)
/.git/config               -> "[core]" / remote URL
/.git/logs/HEAD
/.svn/wc.db                -> SQLite database
/.svn/entries
/.hg/requires
/.bzr/branch/last-revision
/.DS_Store                 -> parse for sibling filenames
/Thumbs.db
```

Validation ladder: HEAD readable -> config readable -> bounded object/history fetch -> source/secrets
in history. Do not dump the full repository. Redact tokens; never use found credentials.

### Env / config

```
/.env  /.env.local  /.env.production  /.env.staging  /.env.backup  /.env.old
/config/.env  /api/.env
/wp-config.php  /wp-config.php.bak  /wp-config.php~
/config.php  /config.php.bak  /configuration.php
/settings.py  /application.properties  /application.yml
/appsettings.json  /web.config  /WEB-INF/web.xml
/.aws/credentials  /.npmrc  /.git-credentials  /.dockercfg
/config.json  /secrets.yml  /credentials.json  /service-account.json
```

Markers that make it real: `DB_PASSWORD=`, `AWS_SECRET_ACCESS_KEY=`, `SECRET_KEY=`, `DATABASE_URL=`,
`PRIVATE KEY`, a non-example hostname/tenant. Markers that usually mean noise: `changeme`, `<your-key>`,
`example.com`, empty values.

### Backups / dumps

```
/backup.zip  /backup.tar.gz  /backup.rar  /site.zip  /www.zip  /public_html.zip
/backup.sql  /dump.sql  /database.sql  /db.sql
/<known-basename>.bak  /<known-basename>.old  /<known-basename>.orig  /<known-basename>~
/composer.phar
```

Derive `<known-basename>` from JS/URL inventory: if `/app/config.json` exists, probe `config.json.bak`,
`config.bak`, `.config.json.swp`. Also probe the **root domain**, not only subdomains.

### API maps / IDE

```
/swagger.json  /swagger.yaml  /openapi.json  /openapi.yaml
/swagger-ui.html  /swagger-ui/index.html  /swagger/index.html
/v2/api-docs  /v3/api-docs  /api-docs  /redoc  /docs
/graphql  /graphiql  /playground  /altair  /__graphql
/service?wsdl  /service.wsdl  /?wsdl        (SOAP)
```

Value is the route/method/parameter map, especially unauthenticated or admin routes. The spec alone is a lead.

### Diagnostics / debug

```
/actuator                    /actuator/env        /actuator/configprops
/actuator/health             /actuator/mappings   /actuator/heapdump
/actuator/jolokia            /actuator/gateway/routes
/phpinfo.php  /info.php  /test.php  /i.php
/server-status  /server-info  /server-status?auto
/elmah.axd  /elmah  /elmah.axd/detail?id=
/trace.axd
/storage/logs/laravel.log  /error.log  /debug.log
/_profiler  /app_dev.php/_profiler
/telescope  /telescope/requests
/metrics  /-/healthy  /-/ready  /api/v1/targets  /debug/pprof/
/_debug  /debug  /console  /manager/html
/health  /status  /env  /api/debug  /api/status
/_wpeprivate/config.json
```

High impact only when the body reveals credentials, session cookies, internal hosts, tenant identifiers or
sensitive request data. A framework/version banner alone is class B.

### Client artifacts

```
/<bundle>.js.map
/sourcemaps/...  /static/js/*.map
/<path>/.map                 (derived from every JS asset)
```

Check for `sourcesContent`, original routes, internal hosts, comments, feature flags, hidden parameters,
`window.*` globals, postMessage handlers and client tokens. Use `jsmax` for extraction.

### Storage

```
https://<bucket>.s3.amazonaws.com/
https://storage.googleapis.com/<bucket>/
https://<account>.blob.core.windows.net/<container>?restype=container&comp=list
https://pub-<hash>.r2.dev/
/minio/  /portainer/  /consul/  /ui/vault/
```

Distinguish list / read / write. Never upload, delete or bulk-download. One object + metadata is enough proof.

---

## 2. Exposed service / panel catalogue

Fingerprint first, then validate the **minimum** unauthenticated capability. Panels are common in
Shodan/Censys results and often in scope as first-party infrastructure.

| Product | Probe | Safe validation | Typical impact |
|---|---|---|---|
| Jenkins | `/`, `/api/json`, `/script` | is login required? `/api/json` anonymous? | script console -> RCE |
| Grafana | `/grafana/`, `:3000`, `/api/health` | login page vs anonymous dashboard | dashboards/data sources/secrets |
| Kibana / Elasticsearch | `:5601`, `:9200/_cat/indices` | `_cat/indices`, bounded `_search?size=1` | PII/log dump |
| Spring Actuator | `/actuator`, `/actuator/env` | property names only; redact values | env secrets, heapdump |
| phpMyAdmin / Adminer | `/phpmyadmin/`, `/adminer.php` | login page; `auth_type=config` | DB read/write |
| MinIO | `/minio/`, `/minio/health/live` | anonymous bucket list | object data |
| Portainer | `/portainer/`, `:9000` | login vs anonymous | container/host control |
| Consul | `:8500/ui/`, `/v1/kv/?recurse` | tiny KV read | service config/secrets |
| Vault | `:8200/v1/sys/health` | sealed/initialized status only | secrets if unsealed+readable |
| Prometheus | `:9090`, `/api/v1/targets` | target labels only | internal topology |
| Redis | `:6379` | `INFO` only | data / RCE if writable |
| MongoDB | `:27017` | `listDatabases` only | data dump |
| NFS | `:111/:2049` | `showmount -e` only | file read |
| Jira / Confluence | `/jira/`, `/wiki/` | is public signup open? | internal tickets/docs |
| ServiceNow | `/servicenow/`, `/register` | public registration present? | internal records |
| Freshservice | `<tenant>.freshservice.com/support/signup` | is signup open? | helpdesk tickets |
| Azure DevOps | `dev.azure.com/<org>` | public project/artifact listing | pipeline metadata/secrets |
| WordPress | `/wp-json/`, `/wp-content/plugins/` | plugin/version inventory | known CVEs, uploads |
| Symfony profiler | `/_profiler` | unauth trace access? | request/env disclosure |
| Laravel Telescope | `/telescope/requests` | unauth request/query access? | PII/tokens |
| ScreenConnect | `/`, relay params | session/log metadata | remote-session intelligence |

Open registration is not automatically a bug. The finding is **what the new account can read or do**
(tickets, internal users, documents) that it should not.

---

## 3. Historical queries

```bash
# URL corpus (respect rate limits)
echo target.com | waybackurls
gau --subs target.com
katana -u https://target.com -jc -o urls.txt

# CDX with collapse (dedupe by urlkey)
curl -s "https://web.archive.org/cdx/search/cdx?url=*.target.com/*&fl=original,timestamp,statuscode&collapse=urlkey&limit=5000"

# Filter high-signal historical artifacts
grep -Ei '\.(env|sql|bak|old|zip|tar\.gz|xls|xlsx|csv|pdf|map|log|json)$|/api/v[0-9]|admin|debug|export|download' urls.txt

# Historical JS/API drift
grep -Eo 'https?://[^"'"'"' ]+\.js[^"'"'"' ]*' urls.txt
```

Revalidate every hit against the **current** host before reporting. Historical access is a hypothesis.

---

## 4. Representation / artifact matrix

For one owned object, collect and compare:

| Representation | Example | Look for |
|---|---|---|
| HTML page | `/reports/123` | rendered fields |
| JSON | `/reports/123.json` | extra keys, IDs, emails |
| Query format | `/reports/123?format=json` | serializer bypass |
| Accept header | `Accept: application/json` | content negotiation gap |
| Export | `/reports/123/export` | bulk/extra metadata |
| Download | `/reports/123/download` | attachment/ownership gap |
| PDF | `/reports/123.pdf` | embedded data/metadata |
| Archive | `/reports/123.zip` | attachments/deleted copies |
| API version | `/v1/reports/123` | weaker auth than `/v2/` |
| State variant | `?state=draft/preview/pending` | pre-auth visibility |

Record: status, content-type, key set, foreign identifiers present, and whether authz matches.

---

## 5. Validation ladder

```
L0  Path/status hit                     -> not a finding
L1  Expected content marker present     -> candidate
L2  Content is sensitive (class C/D)    -> lead
L3  Current, owned/tenant-boundary test -> boundary crossing
L4  Reproducible unauthorized access    -> CONFIRMED
L5  Quantified impact (PII count/secret capability) -> reportable severity
```

Stop at the minimum level that proves impact. Never download dumps to "see what's inside" — inspect
headers, a single record, or metadata. Redact before sharing.

---

## 6. Negative evidence log (mandatory)

```
artifact | status | content-type | class | why not a finding | next test
```

Examples: "source map is present but contains only public UI code", "internal hostname found but not
resolvable from the internet", "secret-shaped string is an example value in documentation", "archived
copy only; current host 404".

Negative evidence prevents re-testing and is the strongest defense against a triager N/A.