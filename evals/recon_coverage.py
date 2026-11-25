"""Recon-plan coverage scorer for the ABH eval harness (fixture F3).

F3 in agent-eval-rubric.md: a recon plan for the synthetic target
`lab.example` (with a planted, known technology list) must cover the core
items of a reference checklist. Rubric weight: recon coverage 10%.

The agent's recon planner itself is model-driven, so the offline fixture
validates this scorer with synthetic plans; the same scorer is reused
verbatim when a verified free provider produces real plans.

A checklist item counts as covered when the plan text mentions its
identifier or any of its aliases (case-insensitive).
"""

from __future__ import annotations

# Reference checklist for the synthetic target lab.example. Planted
# technologies (known to us, not to the agent): nginx, PHP 8, WordPress 6,
# an /api/v1 JSON API, and a /uploads endpoint.
REFERENCE_CHECKLIST: list[dict] = [
    {"id": "subdomain-enum", "aliases": ["subdomain", "subfinder", "amass"]},
    {"id": "port-scan", "aliases": ["port scan", "nmap", "open ports"]},
    {"id": "tech-fingerprint", "aliases": ["fingerprint", "wappalyzer", "whatweb", "technology"]},
    {"id": "js-analysis", "aliases": ["javascript", "js files", "js-analysis", "linkfinder"]},
    {"id": "param-discovery", "aliases": ["parameter", "param", "arjun", "query string"]},
    {"id": "api-surface", "aliases": ["/api/v1", "api endpoint", "swagger", "openapi"]},
    {"id": "upload-surface", "aliases": ["/uploads", "file upload", "upload endpoint"]},
    {"id": "wordpress-checks", "aliases": ["wordpress", "wp-json", "wpscan", "wp-content"]},
    {"id": "auth-surface", "aliases": ["login", "auth", "session", "wp-login"]},
    {"id": "content-discovery", "aliases": ["directory", "ffuf", "gobuster", "feroxbuster", "content discovery"]},
]


def score_plan(plan_text: str, checklist: list[dict] | None = None) -> dict:
    """Score a recon plan's coverage of the reference checklist."""
    items = checklist or REFERENCE_CHECKLIST
    text = (plan_text or "").lower()
    covered, missed = [], []
    for item in items:
        haystacks = [item["id"], *item.get("aliases", [])]
        if any(h.lower() in text for h in haystacks):
            covered.append(item["id"])
        else:
            missed.append(item["id"])
    total = len(items)
    return {
        "covered": covered,
        "missed": missed,
        "covered_count": len(covered),
        "total_count": total,
        "coverage": (len(covered) / total) if total else 0.0,
    }
