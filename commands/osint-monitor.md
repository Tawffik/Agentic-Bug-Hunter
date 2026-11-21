---
description: Delta-first GitHub OSINT monitor for authorized target organizations. Tracks new repos, security-relevant commits, releases, workflow changes, and secret/dependency alerts. Usage: /osint-monitor <org1,org2>
---

# /osint-monitor

```bash
GITHUB_TOKEN=... python3 bughunter/tools/github_osint_monitor.py \
  --orgs "acme,acme-labs" --max-repos 100 --out output/osint
```

Outputs `output/osint/osint-delta.md` / `.json` and updates
`memory/osint-state.json` so later runs show only changes. Read-only; no
cloning or execution. A signal is a LEAD, not a finding.
