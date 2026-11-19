---
description: Bounded information-disclosure / exposure hunt — probes the high-signal artifact catalog (.git/.env/backups/config/Actuator/Swagger/source maps/logs), then validates whether the hit crosses a real visibility boundary. Wraps bughunter/tools/exposure_probe.py (GET-only, SSRF-guarded, LEAD-only) and the web2-exposure skill. Usage: /exposure <url> [--in-scope target.com] [--max-paths N]
---

# /exposure

Turn an exposure hit into a validated finding — or kill it fast.

**Load skill**: `skills/web2-exposure/SKILL.md` (+ `references/artifact-catalog.md`).

## Run this (safe, bounded, LEAD-only)

```bash
# Scan the default catalog (GET only, 0.5s between requests, hard cap 42 paths)
python3 bughunter/tools/exposure_probe.py -u https://target.com

# Scope-gate every request (repeatable pattern)
python3 bughunter/tools/exposure_probe.py -u https://target.com \
  --in-scope target.com --in-scope '*.target.com' --exclude blog.target.com

# Machine-readable for the lead board / memory
python3 bughunter/tools/exposure_probe.py -u https://target.com --json --out exposure.jsonl

# Preview the plan without touching the network
python3 bughunter/tools/exposure_probe.py -u https://target.com --dry-run

# Custom bounded path list (one per line)
python3 bughunter/tools/exposure_probe.py -u https://target.com -l paths.txt --max-paths 20
```

Verdicts: `LEAD` (real content marker), `UNVERIFIED`, `SUSPECT_HTML`, `BLOCKED`, `EMPTY`,
`REDIRECT`, `RATE_LIMIT`, `ERROR`. **Only `LEAD` is worth manual follow-up — none of them is a finding yet.**

## Validate each LEAD

1. Confirm the asset is on the **current** in-scope list and reachable now.
2. Classify sensitivity: A public / B internal / C sensitive / D security-critical.
3. Establish the invariant: who should see this artifact?
4. Capture the minimum proof (headers + one redacted record). Do **not** download dumps.
5. For `.git`/`.svn`: prove reconstruction is possible without dumping history; grep for secrets read-only.
6. For `.env`/config: report key capability, never the value. Do not authenticate with found credentials.
7. For Swagger/OpenAPI: extract only the unauthenticated/admin routes as new hypotheses.
8. For Actuator/phpinfo/Elmah/Telescope: look for secrets, session cookies, internal hosts, env vars.
9. For source maps: hand to `jsmax` (`sourcesContent`, routes, globals, verified secrets).
10. Record **negative evidence** for every non-finding.

## Historical + differential follow-up

- Live 404/403: check Wayback/CDX/URLScan, then revalidate current reachability.
- Compare representations: `/page`, `/page.json`, `?format=json`, `Accept: application/json`,
  `/export`, `/download`, `.pdf`, `.zip`, old `/v1/`.
- Check state variants: draft/preview/pending/archived/shared/deleted/exported.
- Check deletion residue and pending-invitation visibility.

## Handoffs

| Result | Next |
|---|---|
| Source map / JS secret | `jsmax` |
| Bucket/cloud key | `cloud-pentest` |
| Public CI / pipeline metadata | `cicd-security` |
| Chat/support transcript | `agentic-app-audit` (chat reference) |
| Authz edge case | `web2-vuln-classes` (authorization edge cases) |
| Validated | `triage-validation` → `report-writing` |

## Kill signals

- All hits return an HTML shell, login page, or the same 404 template.
- Only framework/version banners, no sensitive data or capability.
- Artifact is public by design (docs, public cert, publishable key) with no impact.
- Historical-only access with no current reachability.
- Secret-shaped string is a placeholder/fixture.