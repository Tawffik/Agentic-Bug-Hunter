# Capability Gaps

> **Update (2026-06-19):** Six gaps from this audit are now **shipped** as
> `tool + slash command + tests` —
> CORS (`/cors`), CRLF/host-header (`/crlf`), NoSQL injection (`/nosqli`),
> JWT attacks (`/jwt-scan`), the OOB blind-bug orchestrator (`/oob`, wraps
> `interactsh-client`), and the LLM red-team corpus runner (`/llm-redteam`).
> Resolved items are marked **✅ SHIPPED** inline below.

> **Update (2026-11-19 — knowledge-base upgrade):** Two new skills close the largest
> knowledge gaps, plus deep references and a new safe tool:
>
> - **`skills/web2-exposure/`** — information disclosure / historical intelligence:
>   artifact catalog, Wayback/CDX/URLScan pivots, representation + artifact-equivalence
>   + state-conditioned + deletion-residue differentials, secrets capability discipline.
> - **`skills/dorking-osint/`** — advanced Google/Bing/GitHub/Shodan/Censys dorks,
>   favicon/cert/copyright pivots, reverse IP/DNS, origin IP, acquisitions, monitoring.
> - **`bughunter/tools/exposure_probe.py`** + `/exposure` — bounded GET-only artifact probe,
>   SSRF/scope-guarded, LEAD-only classifier (no body logging).
> - **`scripts/dork_runner.py`** — new `origin`, `infra`, `github_org`, `saas`, `acquisition`
>   query families.
> - Deep references added under `web2-vuln-classes/references/` (authorization edge cases,
>   parser/403 differentials, framework advisory patterns, SSRF validator desync),
>   `bb-methodology/references/universal-operator-loop.md`, and
>   `report-writing/references/evidence-discipline.md`.
> - Validation: `tests/test_exposure_probe.py`, `tests/test_skills_contract.py`.
>
> Remaining gaps: WebSocket/PostMessage runtime harness, multimodal LLM injection,
> Web3 analyzer wiring, MobSF/Flutter/React-Native depth. CSRF/XXE tooling and iOS playbooks
> shipped 2026-11-19 (`/csrf`, `/xxe`, `mobile-pentest/references/ios-runtime.md`).

Coverage-vs-tooling audit of the plugin (2026-06-19). The repo is **knowledge-rich and
confirmation-poor**: the `skills/*/SKILL.md` docs cover almost every technique, but runtime
automation and out-of-band confirmation are thin. Many vuln classes are "documented but have
no scanner," and several tools are registered in `tools/external_arsenal.sh` as *installable*
but never *wired into the hunt loop*.

Each gap is tagged:

- **[no coverage]** — absent entirely (no skill, no tool).
- **[docs-only]** — explained in a skill, but nothing automates it.
- **[registered-not-wired]** — a tool exists in `external_arsenal.sh` (preloaded/installable)
  but no orchestrator script calls it. **These are the highest-leverage fixes — just wire them.**

> See the [Divert to preloaded tools](#divert-to-preloaded-tools) table at the bottom for the
> quickest wins — gaps that an already-registered tool can close without a new dependency.

---

## Web2 / Web App

**Solid:** 24 vuln classes with bypass tables (IDOR, XSS, SSRF, SQLi, OAuth/OIDC, file upload,
race, business logic, SSTI, smuggling, cache poisoning, MFA/SAML, LFI→RCE, deserialization).
Real runtime scanners exist for XSS/SQLi/SSTI/MFA/SAML (`vuln_scanner.sh`), IDOR
(`h1_idor_scanner.py`, mutation IDOR), race (`h1_race.py`), OAuth (`h1_oauth_tester.py`).

**Missing capabilities:**

- **CORS misconfiguration** — ✅ SHIPPED (`/cors`, `tools/cors_scanner.py`). Previously [docs-only]. One of the most common real bugs; there's
  no automated ACAO-reflection / null-origin / wildcard-credentials tester.
- **NoSQL injection (the "db" surface)** — ✅ SHIPPED (`/nosqli`, `tools/nosqli_scanner.py`):
  operator auth-bypass (`$ne`/`$gt`/`$regex`), bracket-syntax query injection, `$where` time-based
  blind. Was previously uncovered (web2 SQLi tooling is SQL-only).
- **JWT attacks** — ✅ SHIPPED (`/jwt-scan`, `tools/jwt_scanner.py`): alg:none forgery,
  RS256→HS256 confusion, HS256 secret crack, static claim analysis. Was [docs-only] (skill
  documented the bugs; `jwt_tool` registered-not-wired).
- **CSRF** — ✅ SHIPPED (`/csrf`, `tools/csrf_poc.py`): form/multipart/text-plain JSON/method-override/
  GraphQL PoC variants + SameSite/Secure/HttpOnly analyzer (offline). Class 27 in `web2-vuln-classes`.
- **XXE** — ✅ SHIPPED (`/xxe`, `tools/xxe_probe.py`): file/SSRF/OOB-DTD/XInclude/SVG/PHP-filter/UTF-7
  builders + bounded scope-guarded sender. OOB correlation still via `/oob`. Class 28 in `web2-vuln-classes`.
- **CRLF / HTTP response splitting / host-header injection** — ✅ SHIPPED (`/crlf`, `tools/crlf_scanner.py`). Previously [docs-only].
- **Prototype pollution** (server-side + client gadget chains) — only touched by the fuzzer; no
  dedicated detection.
- **WebSocket security** (cross-site WS hijacking, message auth) — ⚠️ PARTIAL: execution playbook
  `web2-vuln-classes/references/websocket-postmessage.md`; runtime harness still manual.
- **HTTP parameter pollution, client-side path traversal, PostMessage** beyond the doc snippet —
  no automation.
- **No headless-browser runtime testing** — ⚠️ PARTIAL: DOM XSS is now confirmable via `/domxss`
  (`tools/dom_xss_harness.py`), which drives headless Chromium (Playwright), injects canary
  payloads into query + fragment params, and reports `[CONFIRMED]` only when the browser actually
  executes them. Client-side prototype pollution and PostMessage still need dedicated probes on
  the same harness. Was [no coverage].

## LLM / AI

**Solid — one of the strongest areas:** prompt injection chains, chatbot IDOR,
markdown/ASCII-smuggling exfil, indirect injection, system-prompt extraction, MCP & RAG
poisoning, full OWASP ASI01–ASI10 agentic coverage. Payload tooling: `hai_probe.py`,
`hai_payload_builder.py`.

**Missing capabilities:**

- **No automated red-team/jailbreak harness** — ✅ SHIPPED (`/llm-redteam`,
  `tools/llm_redteam.py`): categorized corpus (prompt-injection, jailbreak, system-prompt-leak,
  data-exfil, indirect-injection, guardrail-bypass) with canary-token detection. A garak/PyRIT
  integration would still add depth.
- **Multimodal injection** — only text/markdown. No image-embedded-instruction or vision-model
  injection. [no coverage]
- **Model/training-data extraction, embedding-inversion, membership inference** — [no coverage].
- **Denial-of-wallet / token-cost exhaustion** testing — [no coverage].
- **Output-handling bugs** (XSS/SSRF/SQLi via LLM-generated output flowing into a sink) — only the
  markdown-exfil case; no general "LLM output → dangerous sink" tester. [docs-only]
- **Guardrail/filter bypass corpus and multi-turn / crescendo jailbreaks** — not automated.
  [docs-only]

## Agent / autonomous-hunter runtime

**Solid:** ReAct loop, autopilot with circuit breaker + rate limiter + `SafeMethodPolicy`,
deterministic `scope_checker.py`, audit log, pattern DB, 12-provider brain.

**Missing capabilities:**

- **No OOB/blind-bug confirmation** — ✅ SHIPPED (`/oob`, `tools/oob_listener.py`): wraps
  `interactsh-client`, generates per-injection-point payloads for blind SSRF/XXE/SQLi/RCE/Log4Shell
  and correlates inbound DNS/HTTP/SMTP callbacks back to the firing payload. (Was the highest-
  leverage gap.)
- **No Burp/Caido active-scan driving** — the MCP clients proxy traffic but the agent can't
  launch/consume an active scan.
- **No browser automation** in `agent.py` (same gap as Web2).
- **No parallel multi-host hunting** — the loop is sequential.
- **No automatic PoC capture** (screenshot/HAR/video) for reports.
- **No finding-replay/regression** to re-verify past bugs on a target.

## Web3 / Smart Contracts

**Solid:** 10 EVM bug classes + Solana SPL + meme coin + DEX/LP, Foundry PoC templates.

**Missing capabilities:**

- **Static-analyzer / fuzzer integration** — ✅ REGISTERED + INSTALLABLE: `forge/cast/anvil`,
  `slither`, `solc-select`, `crytic-compile`, `aderyn` (retired upstream; existing installs), `echidna`, `medusa`, `halmos`, `mythril`,
  `surya`, `heimdall`, `wake`, `solhint`, `solana/anchor/surfpool` are in
  `bughunter/tools/external_arsenal.sh`; `./install_tools.sh --with-web3` installs them best-effort.
  Web3 MCP configs live in `bughunter/mcp/web3-mcp/` (`foundry-mcp`; `solidity-audit-mcp` built from
  upstream because the npm name is a placeholder). A scripted "run all analyzers + merge findings"
  orchestrator is still manual. [partially closed]
- **Chains beyond EVM + Solana** — no Move (Aptos/Sui), Cairo (Starknet), Vyper, CosmWasm/Cosmos.
  [no coverage]
- **No dedicated bridge / cross-chain class** (one of the highest-paid Web3 categories) — only
  passing mentions. [docs-only]
- **No governance / timelock / DAO-attack class**; no MEV beyond the meme-coin sandwich note.
  [docs-only]

## Mobile

**Solid:** Android-first runtime proxy workflow, APK decompile for secrets/endpoints, deeplink +
exported-activity injection, WebView bridge, SSL-pinning bypass, OkHttp signer recovery.

**Missing capabilities:**

- **iOS is much lighter than Android** — ⚠️ PARTIAL: `mobile-pentest/references/ios-runtime.md` covers
  IPA static sweep, Frida/objection, keychain/NSUserDefaults, ATS/pinning, universal links, WKWebView,
  biometric checks. Automated keychain dump/MobSF wiring is still manual.
- **No MobSF static-scan automation** — `mobsf`, `apkleaks`, `jadx` are [registered-not-wired];
  decompile + grep is manual.
- **No Flutter / React Native specifics** (RN bundle, Reflutter). [no coverage]
- **No local-auth / biometric bypass** or **root/jailbreak-detection bypass** class. [docs-only]

## Recon / Attack Surface

**Solid:** subfinder/chaos/httpx/katana/gau/nuclei pipeline, cloud recon, takeover, secrets,
param discovery, 403 bypass, CVE sweep.

**Missing capabilities:**

- **No active port/service scanning wired in** — ✅ SHIPPED (`/portscan`, `tools/port_scanner.py`):
  wraps `naabu` with an `smap` (passive) fallback and flags the non-web services (Redis, Docker
  API, exposed DBs, RDP, SMB) the HTTP pipeline can't see. Was [registered-not-wired].
- **No visual triage** — ✅ SHIPPED (`/screenshot`, `tools/visual_triage.py`): screenshots live
  hosts via `eyewitness`/`aquatone`/`httpx -screenshot` into a self-contained HTML gallery that
  doubles as report PoC evidence. Was [registered-not-wired].
- **No Shodan/Censys/favicon-hash** asset discovery, **no ASN/CIDR → IP-range** expansion.
  [no coverage]
- **JS source-map extraction / deobfuscation / endpoint extraction** — ✅ SHIPPED
  (`tools/js_analyzer.py`, `/js-analyze`): deterministic offline extractor for endpoints,
  params, secrets (cloud/SaaS/Auth/CI/JWT/keys), client sinks (eval/innerHTML/postMessage/…),
  and source-map refs. `recon_engine.sh` calls it to replace the old inline `sed`+`grep`, and
  `lead_board ingest` already reads `js/endpoints.txt`. `linkfinder` remains optional for
  deeper deobfuscation. Was [registered-not-wired] / [docs-only].

## Cross-cutting / Others

- **SAST source audit** — ✅ SHIPPED (`/sast`, `tools/sast_scan.py`): runs `semgrep` security
  packs over fetched JS/source and normalizes hits into the toolkit's severity + `POSSIBLE`
  confidence model. Was [registered-not-wired]. (A CodeQL ruleset would still add depth.)
- **API-spec-driven testing** — recon ingests OpenAPI/Postman specs, but nothing auto-generates
  IDOR/auth tests from a spec. [no coverage]
- **No thick-client / desktop (Electron-binary), IoT/firmware, or network-pivot** capability —
  likely an intentional scope boundary; confirm and document as such.

---

## Divert to preloaded tools

These gaps already have a tool registered in `tools/external_arsenal.sh`. Closing them is a
**wiring job** (add an orchestrator script + a command), not a new dependency. Highest ROI first.

| Gap | Preloaded tool(s) | What to build |
|---|---|---|
| Blind SSRF / XXE / SQLi / RCE-via-callback | `interactsh-client` | OOB orchestrator: spin up client, inject callback URL, correlate hits into findings |
| Port / service scanning | `naabu`, `smap`, `dnsx` | Add a port-scan phase to `recon_engine.sh`; feed non-HTTP services into the surface |
| SAST source audit | `semgrep` | `sast_scan.sh` over fetched JS/source using the skills' grep patterns as a ruleset |
| Visual triage + PoC screenshots | `eyewitness`, `aquatone` | Screenshot phase in recon; reuse output for report PoC capture |
| Mobile static scan | `mobsf`, `apkleaks`, `jadx` | Wire into `mobile-pentest` as an automated static sweep |
| Mobile runtime (incl. iOS) | `objection` | Scripted pinning-bypass / method-hook recipes |
| DOM/reflected XSS (partial) | `dalfox`, `xsstrike` | Add to `vuln_scanner.sh` XSS phase (still needs a browser for true DOM XSS) |
| JWT attacks | `jwt_tool` | None/alg-confusion/secret-crack helper around the OAuth/auth flow |
| File-upload exploitation | `fuxploider` | Wire into a file-upload testing command |
| WAF detect / bypass | `whatwaf`, `unwaf`, `byp4xx` | Already partly in `bypass_403.sh`; extend with WAF fingerprint gate |

**Genuinely need a new dependency (not preloaded):**

- Headless-browser harness — **Playwright/Selenium** (DOM XSS, client-side, PostMessage,
  multimodal LLM).
- LLM red-team corpus — **garak / PyRIT**.
- Web3 static + fuzzing — **Slither, Aderyn, Echidna, Medusa, Halmos** (none registered yet).
- CORS / CSRF / XXE / CRLF — ✅ purpose-built tooling now exists (`cors_scanner.py`,
  `csrf_poc.py`, `xxe_probe.py`, `crlf_scanner.py`); remaining work is nuclei-template coverage.
