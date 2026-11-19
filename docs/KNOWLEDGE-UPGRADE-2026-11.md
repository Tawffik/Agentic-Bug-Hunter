# Knowledge-Base Upgrade — 2026-11

Source-driven upgrade of the skill corpus from the operator's GitHub knowledge base
(`Tawffik/*`). This document records provenance, the knowledge-to-capability map, and
what was validated — so a future maintainer can audit or extend it without re-reading
every source repo.

> All integrated material is methodology/research guidance for **authorized** testing.
> No source repository was modified. No finding is auto-confirmed: every technique is
> LEAD-only until validated on an in-scope asset with reproducible evidence.

## Sources inspected

| Repo | What was extracted | Where it landed |
|---|---|---|
| `bug-bounty-tips-skills` (333 tips) | full tip corpus: recon/exposure, API authz, auth bypass, IDOR edge cases, dorking, SSRF, password reset, CSRF, XXE, CI/CD, framework advisories, business logic | new `web2-exposure`, `dorking-osint`; deep refs under `web2-vuln-classes`; SSRF/CSRF/XXE/password-reset additions; `scripts/dork_runner.py` families |
| `bug-bounty-tips-playbook` (100-tip export + `tips.json`) | machine-readable tip index, categories, payloads | verified against the 333-tip skill corpus; used for cross-checking |
| `bb-universal-hunting-methodology` | operator loop, Target Graph, invariants, evidence classes, coverage states, output contract | `skills/bb-methodology/references/universal-operator-loop.md` |
| `bb-recon-exposure` | discovery vs validation, asset relationships, historical vs current, recon→hypothesis | `web2-exposure`, `web2-recon` additions |
| `bb-info-disclosure` | visibility-invariant model, disclosure surface map, negative knowledge | `web2-exposure` |
| `bb-ssrf-hunting` | validator/requester desync, redirect hops, inner parser, differential matrix, evidence ladder | `skills/web2-vuln-classes/references/ssrf-validator-desync.md` |
| `bb-chatbot-support-hunting` | chat surface taxonomy, trust boundaries, WS/MQTT authz, third-party widget IDOR, output XSS | `skills/agentic-app-audit/references/chat-support-and-widgets.md` |
| `bb-scan-playbook` | engagement envelope, tech-aware passes, rate defaults, validation checklist, artifacts/run log | applied as discipline in `web2-exposure` / `report-writing` evidence rules |
| `bb-report-template` | CONFIRMED vs NOT EXECUTED chain table, title/impact discipline, rejection checklist | `skills/report-writing/references/evidence-discipline.md` + SKILL section |
| `BugBountyCI` | exposure rules, disclosure desk model, GitHub recon seed corpus, smart-fuzz baseline semantics, detection evidence labels | `scripts/dork_runner.py` families; `web2-exposure` artifact catalog; no CI pipeline code copied |
| `exposure-intelligence` | disclosure taxonomy (ENV/BACKUP/SOURCE_MAP/API_SPEC/VCS/DIAGNOSTIC/TOKEN/HISTORICAL), hunter dorks, artifact paths, API-spec/backup/historical classes | `web2-exposure` artifact catalog + `dorking-osint` dork corpus |
| `security-research-agent` | skill lifecycle discipline (provenance → pattern → procedure → benchmark), "skills are procedures, not the brain" | informs the LEAD/CONFIRMED and negative-evidence gates; not a new skill (would duplicate `bb-methodology`) |
| `web-api-pentest-portfolio` | authorization methodology, API checklist, business-logic playbook | `web2-vuln-classes` BOLA/business-logic sections |
| `ai-agent-security-study` | OWASP LLM/agent curriculum mapping (LLM01-10) | already covered by `llm-redteam`/`agentic-app-audit`; no duplication |
| `dorking-results-`, `targets-recon-results` | sample run artifacts, target-specific notes | reviewed for patterns only; no target data or PII copied |

Not cloned/used: `plamen` (Web3 audit agent), `VulnRadar`, `zero-track-showcase`,
`furniture-commerce-os`, `My-app-`, `chathub-minimal`, `llm-security-guard`,
`security-research-agent-lite`. They were listed during discovery but are either
product code, demos, or redundant with inspected sources. `BugBountyCI` is private
(true) but accessible to the token; it was inspected shallowly (README, methodology,
detection/smart-fuzz docs, exposure rules, seed corpus) rather than executing the
CI pipeline.

## Knowledge-to-capability map (highlights)

| Technique cluster | Before | After |
|---|---|---|
| Exposure artifact families + validation ladder | scattered across recon/omni refs | dedicated `web2-exposure` + catalog + `/exposure` tool |
| Historical intelligence / Wayback/CDX revalidation | mentioned in recon | explicit workflow + artifact catalog |
| Representation / artifact-equivalence / state-conditioned / deletion residue | mostly absent | `web2-exposure` differential families |
| Advanced dorking (Google/Bing/GitHub/Shodan/Censys/favicon/cert/copyright) | `dork_runner.py` (few families) + recon snippets | `dorking-osint` + expanded `dork_runner.py` |
| Reverse IP/DNS, origin IP, acquisition/reverse-whois | partial | `dorking-osint` + `web2-recon` expansion |
| BOLA edge cases (wrapped/array/batch/wildcard/GraphQL mutation/artifact) | skill + omni/johnwick refs partially | canonical `authorization-edge-cases.md` + variant list |
| Parser/routing authorization differentials | one mention | `parser-differential-bypass.md` |
| Framework/advisory-derived patterns | absent | `framework-advisory-patterns.md` |
| SSRF validator/requester desync + inner parser + evidence ladder | bypass tables only | `ssrf-validator-desync.md` + SKILL section |
| CSRF (method override, JSON, GraphQL, SameSite) | docs-only/scattered | class 27 |
| XXE (UTF-7, OOB, SVG/Office, XInclude) | docs-only | class 28 |
| Password-reset edge cases (HPP, newline, token binding, race, response token) | ATO paths 1-5 | ATO paths 6-10 |
| Business logic (entitlement, currency, test cards, last step) | basic | patterns 5-8 |
| Public CI metadata / Azure DevOps / npm remote deps / Actions cache | partial | `cicd-security` section 7b |
| Chat/support/WS/MQTT/widget surface | split across AI skills | unified reference in `agentic-app-audit` |
| Report evidence discipline (CONFIRMED vs NOT EXECUTED) | partial | reference + SKILL section |
| Universal operator loop / Target Graph / coverage states | implicit | explicit reference |

## New / changed components

- Skills: `skills/web2-exposure/`, `skills/dorking-osint/`
- References: `web2-vuln-classes/references/{authorization-edge-cases,parser-differential-bypass,framework-advisory-patterns,ssrf-validator-desync}.md`,
  `bb-methodology/references/universal-operator-loop.md`,
  `report-writing/references/evidence-discipline.md`,
  `agentic-app-audit/references/chat-support-and-widgets.md`
- Tool: `bughunter/tools/exposure_probe.py` (GET-only, SSRF/scope-guarded, content-marker classifier,
  no body logging, LEAD-only)
- Commands: `commands/exposure.md`, `commands/dork.md`
- Scripts: `scripts/dork_runner.py` — `origin`, `infra`, `github_org`, `saas`, `acquisition`
- Routing/docs: `AGENTS.md`, `skills/bug-bounty` routing table, `skills/web2-recon` handoffs,
  `skills/bb-methodology` routing, `docs/CAPABILITY-GAPS.md`, `scripts/README.md`

## Validation performed

```bash
# Targeted
.venv/bin/python -m pytest tests/test_exposure_probe.py tests/test_skills_contract.py -q
# -> 37 passed

# Full suite (includes install-layout, agents frontmatter, memory, scanners)
.venv/bin/python -m pytest -q
# -> 1197 passed

# Syntax
python3 -m py_compile bughunter/tools/exposure_probe.py scripts/dork_runner.py

# Tool smoke (no network)
python3 bughunter/tools/exposure_probe.py -u https://target.com --dry-run --max-paths 5 --json

# Dork generator smoke (new families)
python3 scripts/dork_runner.py -d target.com -c origin
python3 scripts/dork_runner.py -d TargetCorp -c github_org

# Reference integrity: every relative *.md link in skills/*/SKILL.md resolves
# (enforced by tests/test_skills_contract.py::test_relative_markdown_links_resolve)
```

## Safety properties preserved

- No source repo modified; clone-only inspection under `/tmp/gksrc`.
- No secrets committed. `opencode.json` (local, contains a provider key) and `.opencode/`
  (local install) are intentionally left untracked.
- `exposure_probe.py` never prints/stores response bodies; only marker names and status.
- Scope guard (`--in-scope`) and `safe_http` SSRF guard apply to every request/redirect hop.
- All new guidance uses LEAD vs CONFIRMED, negative controls, and explicit stop conditions.

## Known remaining gaps (not addressed by this upgrade)

- No CSRF PoC generator / SameSite analyzer (class now documented).
- No XXE OOB tester beyond `/oob` (class now documented).
- No WebSocket/PostMessage runtime harness; no multimodal LLM injection.
- No Web3 static/fuzz analyzer integration; iOS depth remains lighter than Android.
- Historical dork automation still relies on manual/verified tooling (no scraping engine).