# Master Plan — pro bug-bounty lifecycle, recon/OSINT monitoring, and platform consolidation

> Authorized research only. Every active step must pass `scope_checker.py` and the
> program's rules before touching an asset. No exploitation, credential use, or data
> exfiltration outside the tested scope.

## 1. Objective

Make the portfolio produce **more valid findings and fewer N/A/duplicate submissions**
with a repeatable lifecycle:

```
program intel → asset discovery → OSINT → continuous delta monitoring
→ deep hunt → validation → report → feedback into target scoring
```

The goal is not more scanners. It is **fresh, scoped, evidence-backed leads** that a
human can turn into paid findings.

## 2. Repository portfolio and decisions

| Repo | Decision | Role |
|---|---|---|
| `Agentic-Bug-Hunter` | **Keep — flagship** | Skills, tools, MCP, commands, lifecycle orchestration |
| `VulnRadar` | **Keep — public product** | CVE + OSINT signal feed, daily deltas, public credibility |
| `BugBountyCI` | **Keep — private engine** | Heavy recon/automation, internal only |
| `targets-recon-results` | **Keep — private evidence** | Per-target leads, PoCs, reports, audit trail |
| `bb-*` (8 repos) | **Merge/redirect** | Fold into Agentic; archive standalones |
| `bug-bounty-tips-skills` (333) | **Merge** | Import as `knowledge/tips/` in Agentic; keep a generated index |
| `bug-bounty-tips-playbook` | **Merge/redirect** | Fold into Agentic docs |
| `zero-track-showcase` | **Keep — portfolio** | Sanitized public architecture showcase |
| `exposure-intelligence`, `security-research-agent*` | **Freeze/merge later** | Only if they become the same product |
| `My-app-`, `furniture-commerce-os`, `ai-agent-security-study`, `llm-security-guard`, `chathub-minimal` | **De-prioritize** | Portfolio/learning, not bounty output |

**Rule:** no new repository until the existing four are consolidated and actively used.

## 3. Target architecture

```
                    ┌──────────────────────────────┐
                    │ Agentic-Bug-Hunter           │
                    │ skills · tools · MCP · CLI    │
                    │ lifecycle orchestration       │
                    └──────────────┬───────────────┘
                                   │ adapters / JSON
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼────────┐       ┌─────────▼─────────┐      ┌─────────▼─────────┐
│ Program intel  │       │ Recon/OSINT engine │      │ Deep hunter       │
│ H1/Bugcrowd/   │       │ BugBountyCI · BBOT │      │ auth · object ·   │
│ Intigriti/     │       │ reconFTW · PD tools│      │ logic · chains    │
│ Immunefi       │       └─────────┬─────────┘      └─────────┬─────────┘
└───────┬────────┘                 │                          │
        │                          │                          │
        └───────────────┬──────────┴──────────────────────────┘
                        │
              ┌─────────▼─────────┐
              │ Evidence + state   │
              │ targets-recon-    │
              │ results (private) │
              │ lead board · PoCs │
              └─────────┬─────────┘
                        │
              ┌─────────▼─────────┐
              │ Public signal     │
              │ VulnRadar: CVE +  │
              │ OSINT deltas      │
              └───────────────────┘
```

## 4. Lifecycle stages and deliverables

### Stage 0 — Program intel (before any request)

- Pull scope, payout, program rules, known issues, disclosure history.
- Check duplicate/precedent before hunting: HackerOne, Bugcrowd, Intigriti,
  Immunefi, Solodit, public writeups.
- Score target:
  `score = payout × freshness × auth_surface × business_impact × competition_factor`.
- **Deliverable:** `program-intel.json` + go/no-go with a written kill reason.

### Stage 1 — Asset discovery

- Passive: CT logs, WHOIS/reverse-WHOIS, ASN, acquisitions, GitHub orgs,
  cloud buckets, Wayback/CDX, urlscan, Shodan/Censys.
- Active (scoped only): subfinder, dnsx, httpx, naabu, katana, gau/wayback.
- **Deliverable:** normalized `assets.jsonl` (`host`, `url`, `tech`, `source`,
  `first_seen`, `scope_status`).

### Stage 2 — OSINT and GitHub intelligence

- New repos/commits/releases, CI workflow changes, contributor/org changes.
- Secret/dependency alerts, leaked `.env`/keys, CI artifacts and public metadata.
- Historical endpoints, JS bundles, source maps, mobile/desktop clients.
- **Deliverable:** `osint-delta.md/json` with signal, repo/asset, severity, URL.

### Stage 3 — Continuous monitoring

- Schedule: daily CVE/OSINT deltas; weekly deep asset rescan; on-demand hunt.
- Delta-first: only new/changed assets, endpoints, commits, releases, CVEs, secrets.
- State persisted in repo or private data plane; no self-trigger loops.
- **Deliverable:** one alert per meaningful change, with a kill/verify note.

### Stage 4 — Deep hunt

Prioritize:
1. Fresh assets and changed code/config.
2. Auth flows (OAuth/OIDC/SAML/JWT), object authorization, cross-tenant IDs.
3. Business logic, race windows, state machines, exports/imports.
4. Known bug-class patterns with a concrete target-local trigger.
5. Chains: A→B→C with a named victim and quantified impact.

### Stage 5 — Validation

- 7-Question Gate + 4 validation gates.
- Reproducible PoC (one command), evidence table with `CONFIRMED` vs `NOT EXECUTED`.
- Duplicate/precedent check before writing.
- **Deliverable:** report + PoC + evidence, or a killed lead with reason.

### Stage 6 — Report and feedback

- H1/Bugcrowd/Intigriti/Immunefi template, CVSS 3.1/4.0, impact-first.
- Track outcome: accepted/duplicate/N/A, payout, time spent.
- Feed patterns back into target scoring and validation thresholds.

## 5. Integration matrix

### Tier 1 — implement now

| Integration | Why | Where |
|---|---|---|
| EPSS + CISA KEV + OSV.dev | Exploit likelihood + known exploitation + package advisories | VulnRadar |
| PoC-in-GitHub + Nuclei templates | Public exploit/detector existence | VulnRadar |
| GitHub OSINT monitor | New repos, security commits, workflows, secrets | Agentic (`github_osint_monitor.py`) |
| H1/Bugcrowd/Intigriti/Immunefi APIs | Scope, payout, known issues, duplicates | Agentic |
| Burp/Caido MCP + Playwright | Authenticated traffic, SPA flows, replay | Agentic |
| Solodit/Claudit MCP | Paid precedent + duplicate avoidance | Agentic |
| urlscan + crt.sh + Wayback + Shodan/Censys | Fresh assets, history, origin IPs, exposed services | Recon/OSINT |

### Tier 2 — after Tier 1 is stable

- Secret scanning: GitHub alerts, TruffleHog, gitleaks, Nosey Parker.
- Notifications: Discord/Slack/Telegram deltas only.
- Target scoring service and metrics dashboard.
- Unified evidence schema and state store.
- BBOT/reconFTW/Osmedeus as optional adapters (not forks).

### Tier 3 — only for a concrete need

- Distributed workers (Axiom-style) for huge scopes.
- RAG over Solodit/Cyfrin/DeFiHackLabs for web3 precedent.
- Eval harness/benchmarks for agent quality.
- SpiderFoot/OSINT graph for specialist investigations.

### Explicit non-integrations

- No additional CVE feed without a unique signal.
- No wrapper around a scanner with no evidence model.
- No unmaintained framework, license-incompatible code, or copied agent loop.
- No new repo for every skill or idea.

## 6. GitHub OSINT monitor design (shipped)

`bughunter/tools/github_osint_monitor.py`:

- Inputs: `--orgs`, optional `--max-repos`, `GITHUB_TOKEN`.
- Collects: org repos, latest commit, latest release, Actions workflow hash,
  secret-scanning alerts, Dependabot alerts.
- Diff: state file `memory/osint-state.json`; first run reports new repos and
  current state; later runs only report changes.
- Signals: `new_repo`, `new_commit` (security-keyword severity), `new_release`,
  `workflow_change`, `secret_alert`, `dependabot_alert`.
- Outputs: `output/osint/osint-delta.md` and `.json`.
- Safety: read-only, token-safe, no cloning/execution, delta-only.

Next: add GitHub org lists to target configs and schedule the monitor.

## 7. Target scoring model

```
score = payout_cap
      × freshness (deploy/change in last 30d)
      × auth_surface (OAuth/SSO/object IDs/payments)
      × business_impact (PII/funds/admin)
      × competition_factor (known reports/audits/saturation)
      × confidence (your familiarity/tooling)
```

- Go only if `expected_payout_per_hour` beats the next target.
- Kill quickly: no auth surface, no value, saturated, out-of-scope, or known issue.

## 8. Validation and duplicate discipline

- Duplicate check first: program known issues, H1 Hacktivity, Solodit, public
  advisories, GitHub issues, prior recon notes.
- Evidence ladder:
  `observation → hypothesis → reachability → trigger → impact → PoC → duplicate check`.
- `CONFIRMED` requires a reproducible local/owned-account PoC; otherwise
  `LEAD — NOT EXECUTED`.
- No "could potentially" language. One root cause per report.

## 9. Automation standards

- GitHub-hosted runners only; no custom labels unless a runner is actually registered.
- `permissions: contents: read/write` least privilege.
- `concurrency` with stale-run cleanup; no queued-run starvation.
- Step timeouts; optional enrichment must never block the core job.
- Pin actions to commit SHAs for public repos; cache pip/go/npm.
- Commit state/output only on success/degraded; never self-trigger loops.
- Tests guard workflow validity and output pollution.
- Audit log + rate limits for every active scanner.

## 10. Metrics

| Metric | Target |
|---|---|
| Fresh assets discovered/week | tracked per target |
| Leads → validated findings | > 10% for priority targets |
| Duplicate/N/A rate | < 15% of submissions |
| Time-to-first-signal | < 30 min per recon run |
| Report acceptance | > 70% |
| Payout/hour | improve quarter over quarter |
| Automation success rate | > 95% scheduled runs |

## 11. 30 / 60 / 90-day roadmap

### Days 0–30 — consolidate and stabilize

- [x] Fix VulnRadar runner/concurrency/fingerprint timeout; tests green.
- [x] Add browser capture, patch-diff hunt, pro installer.
- [x] Add GitHub OSINT monitor (`github_osint_monitor.py` + scheduled workflow).
- [x] Add profile/README topics, license, CI badges (VulnRadar).
- [x] Import 333-tip corpus (`knowledge/tips/`) and 7 `bb-*` sources (`knowledge/notion/`) into the flagship.
- [x] Add program-intel adapter (H1/Bugcrowd public stats + target score); known-issues API still needs auth.
- [x] Add EPSS + public-PoC enrichment to VulnRadar; OSV still pending.

### Days 31–60 — lifecycle

- [x] Shared lifecycle schema + BugBountyCI → Agentic handoff (delta state still pending).
- [ ] Target scoring + metrics dashboard.
- [ ] Burp/Caido MCP + Playwright end-to-end capture/replay.
- [ ] Secret scanning + GitHub org monitor schedules.
- [ ] Issue/PR templates, CONTRIBUTING, releases.

### Days 61–90 — results

- [ ] Two deep hunts with validated PoCs (one web2, one web3).
- [ ] Publish sanitized case studies/results.
- [ ] Public VulnRadar live output and monthly report.
- [ ] Reduce N/A/duplicate rate; review payout/hour.

## 12. Risks and guardrails

| Risk | Mitigation |
|---|---|
| Out-of-scope testing | `scope_checker.py` before every request; private scope snapshot |
| Duplicate submissions | Duplicate-first workflow + known-issues check |
| Automation false positives | Evidence gates; LEAD ≠ finding |
| Credential/secret misuse | Read-only by default; no bulk exfil; audit log |
| GitHub rate limits | Token, cache, backoff, delta-only |
| Stale queued workflows | `concurrency` + cancel stale runs + timeouts |
| Fragmentation | One flagship, one public product, one private engine |
| Prompt injection from target content | Treat content as data; no tool execution from fetched text |

## 13. Immediate checklist

1. Merge the 333 tips + `bb-*` skills into `Agentic-Bug-Hunter`.
2. Add program-intel adapter and target scoring.
3. Add EPSS/OSV/PoC-in-GitHub to VulnRadar.
4. Schedule `github_osint_monitor.py` for target orgs.
5. Run one deep hunt (Aiven or Cloudinary) with a validated PoC.
6. Publish a sanitized results page and pin the flagship repos.

---

_This plan is a living document. Update it when a target, integration, or metric changes._
