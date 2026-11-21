# SKILL: Prometheus /metrics + /pprof Exposed → Infrastructure & Runtime Disclosure

**Skill id:** `tip/prometheus-metrics-pprof-exposed-infrastructure-runtime-disclosure`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081e6812fd6947bafc4c8  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Prometheus components and Go services can expose operational metrics, scrape targets, labels, build/runtime metadata, and profiling endpoints. A public /metrics endpoint may reveal internal hostnames, service names, deployment topology, tenant identifiers, queue names, or application behavior; /pprof can reveal detailed runtime profiles and should not be internet-exposed by default. Official Prometheus guidance explicitly warns against exposing component HTTP endpoints publicly. High-signal only when the response reveals sensitive operational context or enables a demonstrated follow-on impact; a reachable endpoint alone may be low impact or out of scope.

## Payload / Code

```
On an explicitly in-scope target, start with low-rate GET checks only on discovered hosts: /metrics, /-/healthy, /-/ready, /api/v1/targets, /api/v1/label/name/values, /debug/pprof/. Do not enumerate aggressively or trigger expensive profiling endpoints. Record only a small redacted sample. Check whether data includes private hostnames, internal IPs, tenant/account identifiers, sensitive labels, or endpoints that expose target metadata. Stop if responses expose customer data or secrets; do not query broad datasets or cause load.
```

## Source

[https://prometheus.io/docs/operating/security/](https://prometheus.io/docs/operating/security/) ; [https://github.com/prometheus/prometheus](https://github.com/prometheus/prometheus) ; [https://bugology.intigriti.io/misconfig-mapper-docs/readme/services](https://bugology.intigriti.io/misconfig-mapper-docs/readme/services)

## Agent execution contract

1. Confirm asset is in authorized scope.
2. Baseline with an account/object you control.
3. Apply **one** mutation from the payload at a time.
4. Discriminate benign explanations (cache, public data, UI-only).
5. Classify as **LEAD** until unauthorized consequence is proven.
6. Stop if real third-party data appears beyond minimal evidence.
7. Hand off to report template only after validation checklist passes.

---
_Synced from Notion Bug Bounty Tips and Tricks · agent skill ready._
