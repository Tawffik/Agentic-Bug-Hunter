# Tools

Python and shell scanner pipeline (~50 tools). Every tool checks whether its
external dependency is installed — missing tools are skipped, never hard-error.

Full catalogue below. Quick start:

```bash
python3 bughunter/tools/hunt.py --target target.com          # recon → leads → scan → report
python3 bughunter/tools/lead_board.py ingest target.com      # after any /recon
python3 bughunter/tools/lead_board.py next target.com        # highest-value untouched lead
bash bughunter/tools/external_arsenal.sh                     # what's installed vs missing
```

---

## Core Pipeline

| Tool | Purpose |
|:---|:---|
| `hunt.py` | Master orchestrator — recon, lead-board ingest, EOL check, vuln scan, optional CVE/zero-day |
| `recon_engine.sh` | Subdomain enum · live host probing · URL crawl · nuclei · CI/CD phase |
| `vuln_scanner.sh` | XSS · SQLi · SSTI · SSRF · MFA · SAML probe pipeline |
| `validate.py` | 4-gate finding validator with identity checks and curl PoC requirement |
| `scope_checker.py` | Deterministic scope safety check before any request |
| `lead_board.py` | Persistent recon→skill lead ledger (`ingest` / `show` / `next` / `touch` / `add`) |

## Recon & Discovery

| Tool | Purpose |
|:---|:---|
| `scope_aggregator.sh` | Multi-platform scope pull (bbscope + bounty-targets-data) |
| `recon_adapter.py` | Normalize recon output across nested/flat layouts |
| `param_discovery.sh` | Hidden HTTP parameters via Arjun · x8 |
| `js_analyzer.py` | Offline JS-bundle analysis — endpoints, params, secrets (cloud/SaaS/Auth/CI/JWT/keys), client sinks, source maps (`analyze <file\|dir\|->`) |
| `cloud_recon.sh` | S3Scanner · cloud_enum · CloudFail for public bucket exposure |
| `takeover_scanner.sh` | Subdomain takeover via dnsReaper · subjack |
| `cve_scan.sh` | Focused nuclei CVE sweep (high/critical) + optional log4j-scan |
| `bypass_403.sh` | Header · method · encoding tricks against 403/401 (soft-block aware) |
| `secrets_hunter.sh` | trufflehog · noseyparker · gitleaks across FS/git/JS/GitHub org |
| `exposure_probe.py` | Bounded GET-only exposure-artifact probe (SSRF/scope-guarded, content-marker classifier, LEAD-only) |
| `exposure_attribution.py` | Attribute OSINT/exposure hits to a target — host relationship + noise triage + disclosure class, ranked leads (LEAD-only) |
| `cicd_scanner.sh` | GitHub Actions workflow scanner (sisakulint + remote scan) |
| `graphql_audit.sh` | 7-phase GraphQL audit: introspection, batching, IDOR, injection, alias bomb |
| `spec_ingest.py` | Ingest OpenAPI 3.x / Swagger 2.0 / Postman into the API surface — routes every declared endpoint to a hunt-* skill (contract-driven, LEAD-only) |
| `eol_check.py` | End-of-life / lifecycle intel from endoflife.date for fingerprint pairs |
| `external_arsenal.sh` | Installed-tool registry (~50 external binaries); `_have <tool>` gate |
| `target_selector.py` | Rank public HackerOne programs and pick top targets |

## WAF / Bypass / Mutation

| Tool | Purpose |
|:---|:---|
| `waf_encoder.py` | Multi-layer encoded payload variants (`--class sqli\|xss\|generic`) |
| `waf_response_analyzer.py` | Score WAF block vs soft-challenge vs real app response |
| `multipart_mutator.py` | Parser-confusion multipart upload variants |
| `sneaky_bits.py` | Invisible Unicode prompt-injection encode/decode (U+2062/U+2064) |

## Client-side & XML

| Tool | Purpose |
|:---|:---|
| `csrf_poc.py` | CSRF PoC generator (form/multipart/text-plain JSON/method-override/GraphQL) + SameSite/Secure/HttpOnly analyzer (offline) |
| `xxe_probe.py` | XXE payload builder (file/SSRF/OOB-DTD/XInclude/SVG/PHP-filter/UTF-7) + bounded scope-guarded sender |

## Fuzzing & Deep Probes

| Tool | Purpose |
|:---|:---|
| `zero_day_fuzzer.py` | Smart fuzzing + edge-case / logic-flaw probes (manual verify required) |
| `hai_payload_builder.py` | VAPT payload library + LLM injection generator |
| `hai_probe.py` | Fingerprint HackerOne AI Copilot / Hai API surface |
| `hai_browser_recon.js` | Browser-side Hai recon helper |

## IDOR / Auth / Race (H1-style dual-session)

| Tool | Purpose |
|:---|:---|
| `h1_idor_scanner.py` | Cross-user GraphQL IDOR — Account B token vs Account A IDs |
| `h1_mutation_idor.py` | Privileged mutation IDOR battery |
| `h1_oauth_tester.py` | OAuth state CSRF, redirect_uri, 2FA, pre-ATO, host-header reset |
| `h1_race.py` | Race conditions (double-spend, 2FA rate limits, parallel actions) |
| `h1_run.sh` | Convenience wrapper for the H1 dual-session suite |
| `zendesk_idor_test.py` | Zendesk org-boundary IDOR / BAC tester |

## Web3

| Tool | Purpose |
|:---|:---|
| `token_scanner.py` | Automated token red-flag scanner (EVM + Solana / Anchor) |
| `web3_evm_hazard_scan.py` | LEAD-only scanner: payable multicall/msg.value reuse + L2 dialect hazards (`--json`) |
| `defi_hack_search.sh` | Search a local DeFiHackLabs clone for runnable exploit PoCs by term |
| `chain_audit_env.sh` | Detect EVM/Solana/aptos/Sui/Soroban/DAML project and print build/test/fuzz commands (`--json`) |
| `xray_git_security.py` | Pre-audit git-history risk: fix commits, guard changes, dangerous-area churn (`--json`) |

## Pro Workflow / Browser / Cloud / Mobile

| Tool | Purpose |
|:---|:---|
| `browser_capture.py` | Playwright authenticated capture: network requests, storage, cookies, screenshot, HAR, replayable storage state |
| `patch_diff_hunt.sh` | Fix/CVE commit range → changed files, guard diffs, sibling-path hypotheses, report |
| `github_osint_monitor.py` | Delta-first GitHub org monitor: new repos, security commits, releases, workflow changes, secret/dependency alerts |
| `program_intel.py` | Public HackerOne/Bugcrowd stats + 0-100 target score |
| `handoff_ingest.py` | Validate/dedupe/rank a BugBountyCI `agent-handoff/` and optionally ingest into the lead board |
| `dom_xss_harness.py` | Real-browser DOM XSS confirmation (requires Playwright + Chromium) |
| `auth_session.py` / `_auth_helper.sh` | Load once, inject auth into curl/httpx/katana/nuclei/ffuf |
| `aws` / `gcloud` / `az` | Cloud post-access and IAM enumeration (install separately) |
| `adb` / `frida` | Android runtime capture and SSL-pinning bypass (authorized mobile scope) |
| `mitmproxy` | Traffic capture/replay when Burp/Caido is not available |

Install these with `./install_tools.sh --with-pro` (browser, AWS CLI, mitmproxy,
adb, Frida; gcloud/az are printed as separate installs).

## Intelligence & Planning

| Tool | Purpose |
|:---|:---|
| `intel_engine.py` | CVE + disclosure intel with hunt-memory context |
| `self_audit.py` | Continuous-evolution engine — capability inventory, coverage-gap detection, test-regression drift vs baseline, and an improvement ledger with measured metrics |
| `learn.py` | On-demand target learning from disclosed reports / NVD / GHSA |
| `mindmap.py` | Mermaid mind map + prioritized hunting checklist from tech stack |
| `dashboard.py` | Live ANSI TUI for recon/hunt phase progress |
| `banner.py` / `banner.sh` | Shared CLI banner (gradient BUGHUNTER logo) |

## Memory & Session

| Tool | Purpose |
|:---|:---|
| `memory_gc.py` | Inspect and rotate hunt-memory JSONL files (10 MB cap, 3 backups) |
| `auth_session.py` | Auth header management across all tools (`--cookie` / `--bearer` / `--auth-file`) |
| `credential_store.py` | Encrypted / `.env`-backed credential store for hunt sessions |
| `_auth_helper.sh` | Bash helper that injects `BBHUNT_AUTH_*` into curl/httpx children |

## Credential Attack (requires `--with-credential-attack`)

| Tool | Purpose |
|:---|:---|
| `wordlist_engine.sh` | Company-specific password wordlist (cewler + hashcat rules) |
| `osint_employees.sh` | Employee names + emails (theHarvester + username-anarchy) |
| `breach_checker.py` | HIBP k-anonymity ranking by real-world breach count |
| `spray_orchestrator.sh` | Password spray with typed-host confirm + lockout warn + audit log |
| `_spray_http_form.py` | HTTP form spray worker (spawned by orchestrator) |
| `_spray_oauth.py` | OAuth password-grant spray worker |

## Additional Scanners & Support

| Tool | Purpose |
|:---|:---|
| `cors_scanner.py` | CORS misconfiguration (origin reflection / null / credentialed read) |
| `crlf_scanner.py` | CRLF & host-header injection |
| `jwt_scanner.py` | JWT attacks (alg:none, RS256→HS256 confusion, secret crack) |
| `nosqli_scanner.py` | NoSQL injection (operator auth-bypass / `$where` blind) |
| `oob_listener.py` | Out-of-band confirmation of blind SSRF/XXE/SQLi/RCE via interactsh |
| `llm_redteam.py` | LLM red-team corpus (prompt injection / jailbreak / prompt leak / exfil) |
| `sast_scan.py` | Lightweight source SAST for the argument→sink classes |
| `port_scanner.py` | Focused service/port sweep for recon |
| `visual_triage.py` | Rank screenshots/findings for human triage |
| `poc_bundler.py` | Bundle PoC + evidence into a submission artifact |
| `oracle.py` | Deterministic oracle helpers backing verification gates |
| `verifier.py` | Per-lead deterministic verifier used by swarm workers |
| `swarm.py` | Parallel ephemeral verifiers over the lead board |
| `memory_migrate.py` | Migrate/rotate hunt-memory JSONL between schemas |
| `hunt_dashboard.py` | Live ANSI dashboard for hunt state |
| `target_normalize.py` | Safe target/dir-name normalization (path-traversal guard) |
| `banner.sh` | Shared CLI banner helper sourced by tools |

## Output Format

Scanner confidence states prepended to every finding:

- `[CONFIRMED]` — PoC-verified, real impact demonstrated
- `[POSSIBLE]` — strong signal, needs manual verification
- `[INFORMATIONAL]` — version/banner/config data, not a vulnerability

## Post-recon ritual (never skip)

```bash
python3 bughunter/tools/lead_board.py ingest target.com
python3 bughunter/tools/lead_board.py show target.com
python3 bughunter/tools/lead_board.py next target.com
# then route: GraphQL → hunt-graphql /skills/graphql-audit, etc.
```

`hunt.py` runs `lead_board ingest` + EOL check automatically after recon unless
`--skip-leads` is set.
