# SKILL: Bug Bounty Scan Playbook

**Name:** `bb-scan-playbook`  
**Version:** 1.0  
**Source:** Notion — *Bug Bounty Scan Playbook — Professional Template*  
**Purpose:** Reusable, tech-aware, engagement-ready scan template for authorized programs. Evidence-based, scope-strict, rate-respectful, report-ready.

> Not a full app pentest. Not proof of security if zero findings. Authorized assets only.

## When to use

- Opening a new program engagement
- Structuring a bounded automated + manual scan pass
- Logging findings and validation before reporting
- Capturing artifacts paths and run log for auditability

## Engagement meta (fill first)

| Field | Value |
| --- | --- |
| Program / Org | |
| Platform | Intigriti / HackerOne / Bugcrowd / Private |
| Program URL | |
| Researcher handle | |
| Scan ID | `SCAN-YYYYMMDD-001` |
| Start / End (UTC) | |
| Authorization proof | ticket / email / program rules |
| Safe harbor confirmed | ☐ Yes |

Rules of engagement (from program): max rate, allowed hours, forbidden actions, reporting channel.

## Scope

- **In-scope assets table:** Asset | Type | Notes | Bounty tier
- **Explicitly out of scope**
- Special constraints (no scanners on contact forms, no credential stuffing, PII handling)

## Target inventory

- `targets.txt` (one host per line)
- Counts: supplied / HTTP responsive / skipped

## Fingerprint & technology map

After live probe (`httpx` or equivalent):

| Host | URL | Status | Title | Server | CDN/WAF | Technologies | Notes |

**Tech → template strategy**

| Detected stack | Preferred tags / focus | Priority |
| --- | --- | --- |
| Generic web | cve, exposure, misconfig, panel | High |
| Login / SSO | default-login, auth panels, token exposure | High |
| File transfer products | product-specific + exposure | High |
| Monitoring products | product tags + default creds | Medium |
| Unknown | automatic-scan + severity filter | Medium |

## Scan methodology pipeline

### Phase A — Recon (optional, scope-gated)

- [ ] Passive subs (subfinder / CT)
- [ ] DNS resolve (dnsx)
- [ ] Port scan top ports (naabu) — **only if in scope**
- [ ] Live HTTP probe (httpx)
- [ ] Crawl / historical URLs (katana / gau) — if allowed

### Phase B — Tech-aware vulnerability scan

1. **Pass 1 — Automatic** (medium+; exclude dos/fuzz/intrusive)
2. **Pass 2 — High-value tags** (cve, exposure, misconfig, default-login, panel)
3. **Pass 3 — Stack-specific** (from fingerprint table)

### Rate & safety defaults

| Setting | Conservative | Balanced | Aggressive (approval only) |
| --- | --- | --- | --- |
| rate-limit | 5–8 | 15–30 | 50+ |
| concurrency | 5–8 | 15–25 | 50+ |
| retries | 1 | 1–2 | 0–1 |
| timeout | 10–12s | 10s | 5–8s |

Recommended header: `X-Bug-Bounty: <handle>`

## Findings log

| # | Severity | Host/URL | Template ID | Title | Status | Validated | Report ID |

Severity triage:
- Critical: RCE, admin auth bypass, mass PII
- High: significant data exposure, privilege escalation
- Medium: limited exposure with clear impact
- Low/Info: hardening (often OOS)

## Validation checklist (before report)

- [ ] Reproducible with minimal steps
- [ ] In-scope asset only
- [ ] Impact in business terms
- [ ] FP ruled out
- [ ] No destructive testing
- [ ] Evidence redacted
- [ ] Suggested remediation
- [ ] Matches accepted vuln types

## Report draft skeleton

Title → Severity → Asset → Description → Steps → Proof → Impact → Remediation → References

## Artifacts table

targets.txt · httpx JSONL · scanner findings · coverage.csv · report · screenshots · ZIP

## Run log

Timestamp | Action | Result | Notes

## Risks & blockers

WAF/rate limits · 403/401 walls · scope ambiguity · tool issues

## Agent output contract

1. Confirm envelope + in-scope list before any active scan
2. Produce fingerprint table before tag selection
3. Log every pass with counts
4. Never mark validated without the validation checklist
5. Prefer LEAD classification until human confirms
