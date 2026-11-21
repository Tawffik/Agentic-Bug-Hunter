#!/usr/bin/env python3
"""exposure_attribution.py — attribute OSINT / exposure hits to the target.

The gap this closes: `scripts/dork_runner.py` (and raw GitHub/URLScan/CDX/Google
results) produce *hits*, but nothing decides whether a hit actually belongs to
the target organisation or is third-party noise (localhost, example.com,
node_modules, vendor templates). AGENTS.md advertises a "attribution gate" on
`/dork` that did not exist in code. This is that gate, made deterministic and
testable.

It answers three questions per hit, offline and without contacting anything:
  1. Relationship — is the host the target, a subdomain, or unrelated?
  2. Noise        — is it a known non-signal (localhost/example/vendor/template)?
  3. Class        — what kind of disclosure does the path/text suggest
                    (env/config, backup, source map, API spec, VCS, diagnostic,
                    secret-like, historical, generic) and what is the next step?

Output is a ranked, deduped lead list with an explicit verdict:
TARGET | LIKELY | WEAK | NOISE | UNRELATED — never a confirmed finding.

Relationship is a technical signal only: it is NOT authorization and NOT
vulnerability proof.

Usage:
  python3 bughunter/tools/exposure_attribution.py attribute --target acme.com -i hits.jsonl --json
  python3 bughunter/tools/exposure_attribution.py attribute --target acme.com -i hits.jsonl --min-verdict LIKELY
  cat hits.jsonl | python3 bughunter/tools/exposure_attribution.py attribute --target acme.com -
  python3 bughunter/tools/exposure_attribution.py classify --url https://acme.com/.env
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urlparse

# ── hostname helpers ────────────────────────────────────────────────────────

# A small, pragmatic set of two-label public suffixes (enough to compare
# registrable domains without a full PSL dependency).
_TWO_LABEL_SUFFIXES = {
    "co.uk", "org.uk", "gov.uk", "ac.uk", "co.jp", "ne.jp", "or.jp",
    "com.au", "net.au", "org.au", "com.br", "com.cn", "com.tw", "com.hk",
    "co.in", "co.nz", "co.za", "com.mx", "com.tr", "com.sg", "co.kr",
}


def normalize_hostname(host: str) -> str:
    h = (host or "").strip().lower()
    if h.startswith("[") and h.endswith("]"):
        h = h[1:-1]
    return h.rstrip(".")


def hostname_from_url(url: str) -> str | None:
    u = (url or "").strip()
    if not u:
        return None
    if "://" not in u:
        # bare host[:port] — require it look like a hostname
        candidate = u.split("/", 1)[0]
        candidate = candidate.split(":", 1)[0]
        if not candidate or " " in candidate or "." not in candidate:
            return None
        return normalize_hostname(candidate)
    try:
        host = urlparse(u).hostname
    except ValueError:
        return None
    if not host:
        return None
    host = normalize_hostname(host)
    return host or None


def is_subdomain_of(host: str, parent: str) -> bool:
    """Label-boundary safe: notacme.com is NOT under acme.com."""
    h, p = normalize_hostname(host), normalize_hostname(parent)
    if not h or not p:
        return False
    return h == p or h.endswith("." + p)


def registrable_domain(host: str) -> str:
    parts = normalize_hostname(host).split(".")
    if len(parts) <= 2:
        return ".".join(parts)
    if ".".join(parts[-2:]) in _TWO_LABEL_SUFFIXES:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def target_label(target: str) -> str:
    """The brand label of the target (acme.com -> 'acme') for textual match."""
    rd = registrable_domain(target)
    return rd.split(".")[0] if rd else ""


def relationship(target: str, url: str) -> dict:
    host = hostname_from_url(url)
    t = normalize_hostname(target)
    if not host:
        return {"relationship": "UNATTRIBUTED", "host": "", "textual_match": bool(
            target_label(t) and target_label(t) in (url or "").lower())}
    if host == t:
        rel = "DIRECT_HOST"
    elif is_subdomain_of(host, t):
        rel = "RELATED_SUBDOMAIN"
    else:
        rel = "INDEX_ONLY"
    label = target_label(t)
    textual = bool(label and label in host.replace(t, ""))
    return {"relationship": rel, "host": host, "textual_match": textual}


# ── noise ───────────────────────────────────────────────────────────────────

_NOISE_HOST_RE = re.compile(
    r"^(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|.*\.local|.*\.localhost|"
    r".*\.(?:example|test|invalid|example\.[a-z]+))$", re.I)
_NOISE_PATH_RE = re.compile(
    r"(?:/node_modules/|/bower_components/|/vendor/|/wp-content/plugins/|"
    r"/wp-includes/|/site-packages/|/\.git/(?!config)|"
    r"\.env\.(?:example|sample|template|dist|mock|copy)|example\.env|"
    r"\.env-sample|/examples?/|/fixtures?/|/__mocks__/|/demo-store/|"
    r"sample-app|placeholder|dummy[-_.])", re.I)
_NOISE_TEXT_RE = re.compile(
    r"(?i)(?:localhost|127\.0\.0\.1|changeme|your[_-]?api[_-]?key|<your|"
    r"example\.[a-z]{2,}|test@example|foo@bar)")


def detect_noise(url: str, text: str = "") -> list[str]:
    host = hostname_from_url(url) or ""
    blob = (url or "") + "\n" + (text or "")
    reasons = []
    if _NOISE_HOST_RE.match(host):
        reasons.append("noise_host")
    if _NOISE_PATH_RE.search(blob):
        reasons.append("noise_path")
    if _NOISE_TEXT_RE.search(text or ""):
        reasons.append("noise_text")
    return reasons


# ── disclosure class (text/path based; complements exposure_probe markers) ──

_CLASS_RULES = [
    ("VCS_METADATA", re.compile(r"/\.git(?:/|$)|/\.svn(?:/|$)|ref:\s*refs/|\.git/config", re.I),
     "Exposed VCS metadata can enable source reconstruction; confirm reachability, don't dump repos."),
    ("ENV_CONFIG", re.compile(r"\.env(?:\b|\.)|wp-config\.php|appsettings\.json|/config\.json|credentials(?:\.json)?\b|application\.(?:yml|properties)|secrets\.ya?ml", re.I),
     "Config/.env artifact may expose credentials/internal hosts; review redacted keys only."),
    ("BACKUP_DUMP", re.compile(r"\.(?:zip|tar\.gz|tgz|sql|bak|old|orig)(?:\b|$)|backup|dump|db\.sql|database\.sql", re.I),
     "Archive/dump may contain source/PII; confirm sensitivity offline, do not bulk-download."),
    ("SOURCE_MAP", re.compile(r"\.map(?:\b|$)|sourceMappingURL", re.I),
     "Source map may reveal original source + embedded secrets; inspect for endpoints/keys."),
    ("API_SPEC", re.compile(r"openapi|swagger|/api-docs|/v[0-9]+/swagger", re.I),
     "Spec maps hidden/auth routes; derive unauthenticated routes as follow-up hypotheses."),
    ("DIAGNOSTIC", re.compile(r"/actuator|phpinfo|/debug\b|/trace\b|/server-status|/heapdump|/env\b(?!\.)|/metrics\b", re.I),
     "Diagnostics leak env/paths/versions; capture redacted evidence, avoid invasive probing."),
    ("SECRET_LIKE", re.compile(r"\bAKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_|glpat-|sk_(?:live|test)_|xox[baprs]-|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|AIza[0-9A-Za-z_\-]{35}|whsec_|npm_[A-Za-z0-9]{20,}", re.I),
     "Secret-like token pattern; report the pattern/type only — never authenticate with it."),
]

_HISTORICAL_SOURCES = {"cdx", "wayback", "urlscan", "archive", "commoncrawl"}


def classify_disclosure(url: str = "", text: str = "", source: str = "") -> dict:
    blob = (url or "") + "\n" + (text or "")
    for name, rx, human_next in _CLASS_RULES:
        if rx.search(blob):
            return {"class": name, "confidence": "high" if text else "medium",
                    "human_next": human_next}
    if (source or "").lower() in _HISTORICAL_SOURCES:
        return {"class": "HISTORICAL_INDEX", "confidence": "low",
                "human_next": "Historical/index evidence only — verify current reachability under scope."}
    return {"class": "GENERIC_PUBLIC", "confidence": "low",
            "human_next": "Deprioritize unless relationship evidence is strong."}


# ── scoring ─────────────────────────────────────────────────────────────────

_REL_SCORE = {"DIRECT_HOST": 60, "RELATED_SUBDOMAIN": 50, "INDEX_ONLY": 25, "UNATTRIBUTED": 10}
_HIGH_CLASSES = {"ENV_CONFIG", "BACKUP_DUMP", "VCS_METADATA", "SECRET_LIKE"}


def score_hit(target: str, hit: dict) -> dict:
    url = str(hit.get("url") or hit.get("location") or hit.get("host") or "")
    text = str(hit.get("snippet") or hit.get("text") or hit.get("body") or "")
    source = str(hit.get("source") or "")
    rel = relationship(target, url)
    noise = detect_noise(url, text)
    disc = classify_disclosure(url, text, source)

    score = _REL_SCORE.get(rel["relationship"], 10)
    if rel.get("textual_match"):
        score += 10
    if disc["class"] in _HIGH_CLASSES:
        score += 30
    reasons = [rel["relationship"], f"class:{disc['class']}"]
    if noise:
        score -= 40
        reasons += [f"noise:{n}" for n in noise]
    score = max(0, min(100, score))

    host_noise = "noise_host" in noise
    content_noise = ("noise_path" in noise) or ("noise_text" in noise)
    if score >= 70 and rel["relationship"] in ("DIRECT_HOST", "RELATED_SUBDOMAIN"):
        verdict = "TARGET"
    elif score >= 50:
        verdict = "LIKELY"
    elif score >= 25:
        verdict = "WEAK"
    else:
        verdict = "UNRELATED"

    if host_noise:
        verdict = "NOISE"
    elif noise and rel["relationship"] in ("INDEX_ONLY", "UNATTRIBUTED"):
        verdict = "NOISE"
    elif content_noise and verdict in ("TARGET", "LIKELY"):
        # template/example/vendor path on a real host — not an exposure
        verdict = "WEAK"

    return {
        "url": url,
        "host": rel["host"],
        "relationship": rel["relationship"],
        "disclosure_class": disc["class"],
        "verdict": verdict,
        "score": score,
        "reasons": reasons,
        "human_next": disc["human_next"],
        "confirmed_vulnerability": False,
    }


_VERDICT_RANK = {"TARGET": 0, "LIKELY": 1, "WEAK": 2, "NOISE": 3, "UNRELATED": 4}
# Higher = more relevant. Default --min-verdict WEAK therefore drops noise.
_VERDICT_ORDER = {"UNRELATED": 0, "NOISE": 1, "WEAK": 2, "LIKELY": 3, "TARGET": 4}


def attribute_hits(target: str, hits: list[dict], min_verdict: str = "WEAK") -> list[dict]:
    floor = _VERDICT_ORDER.get(min_verdict.upper(), 1)
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for hit in hits:
        scored = score_hit(target, hit)
        key = (registrable_domain(scored["host"] or ""), urlparse(scored["url"]).path if "//" in scored["url"] else scored["url"])
        if key in seen:
            continue
        seen.add(key)
        if _VERDICT_ORDER.get(scored["verdict"], 0) >= floor:
            out.append(scored)
    out.sort(key=lambda d: (_VERDICT_RANK.get(d["verdict"], 9), -d["score"], d["url"]))
    return out


def _iter_hits(text: str):
    text = (text or "").strip()
    if not text:
        return
    if text.startswith("["):
        for row in json.loads(text):
            if isinstance(row, dict):
                yield row
        return
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            row = {"url": line}
        if isinstance(row, dict):
            yield row


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Attribute OSINT/exposure hits to a target (LEAD-only).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("attribute", help="score + rank a batch of hits")
    pa.add_argument("--target", required=True)
    pa.add_argument("-i", "--input", default="-", help="hits file (JSON array or JSONL), or - for stdin")
    pa.add_argument("--min-verdict", default="WEAK",
                    choices=["TARGET", "LIKELY", "WEAK", "NOISE", "UNRELATED"])
    pa.add_argument("--json", action="store_true")
    pa.add_argument("--out", default="")

    pc = sub.add_parser("classify", help="classify one URL/text")
    pc.add_argument("--url", default="")
    pc.add_argument("--text", default="")
    pc.add_argument("--source", default="")
    pc.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd == "classify":
        res = classify_disclosure(args.url, args.text, args.source)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"class: {res['class']} ({res['confidence']})")
            print(f"next:  {res['human_next']}")
        return 0

    text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8", errors="replace").read()
    ranked = attribute_hits(args.target, list(_iter_hits(text)), args.min_verdict)
    summary = {
        "target": args.target,
        "min_verdict": args.min_verdict,
        "leads": len(ranked),
        "by_verdict": {v: sum(1 for r in ranked if r["verdict"] == v) for v in _VERDICT_RANK},
        "results": ranked,
    }
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            for r in ranked:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    if args.json:
        print(json.dumps(summary, indent=2))
        return 0
    print(f"target: {args.target}  leads: {len(ranked)}  ({summary['by_verdict']})")
    for r in ranked[:25]:
        print(f"  [{r['verdict']:>9}] {r['score']:>3}  {r['disclosure_class']:<14} {r['url'][:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
