#!/usr/bin/env python3
"""js_analyzer.py — deterministic JavaScript bundle analysis (offline).

Closes the capability gap "No JS source-map extraction / deobfuscation beyond
secret-grepping" (docs/CAPABILITY-GAPS.md): recon_engine.sh used a one-line
`sed`/`grep` to pull endpoints and a fixed secret regex out of the top-50 JS
files. This replaces that duplication with one tested extractor that pulls:

  * endpoints      — app paths + absolute URLs found in string/template literals
  * parameters     — query-parameter names surfaced anywhere in the bundle
  * secrets        — cloud/SaaS/Auth/CI key patterns + JWTs + private keys
  * client sinks   — eval / innerHTML / postMessage / document.write / ...
  * source maps    — //# sourceMappingURL=, //# sourceURL=

Pure and offline: it only reads files/stdin and never sends a request, so it is
fully unit-testable and safe to point at any bundle. The fetching (with auth)
stays where it already lives — recon_engine.sh — which then calls this to do the
analysis.

Usage:
  python3 bughunter/tools/js_analyzer.py analyze ./js_dir --out recon/t/js --json
  python3 bughunter/tools/js_analyzer.py analyze app.js
  curl -s https://t/app.js | python3 bughunter/tools/js_analyzer.py analyze - --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ── extraction patterns ─────────────────────────────────────────────────────

# A quoted string literal that is a rooted path but not a protocol-relative URL.
# Allows an optional query/fragment so the full literal is seen, then normalized.
_PATH_RE = re.compile(
    r"""["'`](/(?!/)[A-Za-z0-9._~!$&'()*+,;=:@%?\-]+(?:[/?&=%#][A-Za-z0-9._~!$&'()*+,;=:@%?\-]*)*)["'`]"""
)
_ABSOLUTE_URL_RE = re.compile(r"""https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%\-]+""")
_QUERY_PARAM_RE = re.compile(r"[?&]([A-Za-z_][A-Za-z0-9_]{0,40})=")
_SOURCEMAP_RE = re.compile(r"//#\s*sourceMappingURL=([^\s'\"]+)")
_SOURCEURL_RE = re.compile(r"//#\s*sourceURL=([^\s'\"]+)")

# Asset extensions that are never app endpoints — filtered out of the path set.
_ASSET_EXT = re.compile(
    r"\.(?:png|jpe?g|gif|svg|ico|webp|woff2?|ttf|eot|css|less|scss|mp4|webm|pdf|zip)(?:\?|$)",
    re.I,
)

# (label, compiled regex). Ordered most-specific first so a token is classed once.
_SECRET_PATTERNS = [
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("stripe_secret", re.compile(r"\bsk_(?:live|test)_[0-9a-zA-Z]{16,}\b")),
    ("stripe_publishable", re.compile(r"\bpk_(?:live|test)_[0-9a-zA-Z]{16,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b")),
    ("slack_webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[A-Za-z0-9]+")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("gitlab_token", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("twilio_sid", re.compile(r"\bAC[0-9a-fA-F]{32}\b")),
    ("sendgrid_key", re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b")),
    ("mailgun_key", re.compile(r"\bkey-[0-9a-zA-Z]{32}\b")),
    ("discord_webhook", re.compile(r"https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_\-]+")),
    ("firebase_url", re.compile(r"https://[a-z0-9-]+\.firebaseio\.com")),
    ("s3_bucket", re.compile(r"\b[a-z0-9.\-]{3,63}\.s3(?:[.-][a-z0-9-]+)?\.amazonaws\.com\b")),
    ("generic_secret", re.compile(
        r"""(?i)["']?(?:api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token|"""
        r"""client[_-]?secret|secret[_-]?key|password|passwd|pwd)["']?\s*[:=]\s*["']([A-Za-z0-9_\-]{8,})["']"""
    )),
]

# Client-side sink indicators → count of occurrences (lead hints, not proof).
_SINKS = [
    ("eval", re.compile(r"\beval\s*\(")),
    ("new_Function", re.compile(r"\bnew\s+Function\s*\(")),
    ("innerHTML", re.compile(r"\.innerHTML\s*=")),
    ("dangerouslySetInnerHTML", re.compile(r"dangerouslySetInnerHTML")),
    ("document_write", re.compile(r"document\.write\s*\(")),
    ("postMessage", re.compile(r"\.postMessage\s*\(")),
    ("message_listener", re.compile(r"""addEventListener\(\s*["']message["']""")),
    ("location_assign", re.compile(r"(?:location\.href\s*=|location\.assign\s*\()")),
    ("setTimeout_string", re.compile(r"\bset(?:Timeout|Interval)\s*\(\s*[\"'`]")),
    ("node_child_process", re.compile(r"child_process|\bexecSync\b|\bspawnSync\b")),
]

_MAX_TEXT = 8_000_000  # guard against a pathologically huge bundle


@dataclass
class Finding:
    kind: str      # secret | sink | sourcemap | ...
    value: str
    source: str = ""


def _is_noise_path(path: str) -> bool:
    if len(path) < 2 or path.startswith("//"):
        return True
    if _ASSET_EXT.search(path):
        return True
    # a single-segment path of a common static asset dir is low value
    if path.count("/") <= 1 and path.rstrip("/") in ("", "/"):
        return True
    return False


def extract_paths(text: str) -> set[str]:
    paths = set()
    for m in _PATH_RE.finditer(text or ""):
        raw = m.group(1)
        clean = raw.split("?", 1)[0].split("#", 1)[0]
        if not _is_noise_path(clean):
            paths.add(clean)
    return paths


def extract_urls(text: str) -> set[str]:
    return set(_ABSOLUTE_URL_RE.findall(text or ""))


def extract_params(text: str, urls: set[str] | None = None) -> set[str]:
    params = set(_QUERY_PARAM_RE.findall(text or ""))
    for u in urls or ():
        params |= set(_QUERY_PARAM_RE.findall(u))
    return params


def extract_secrets(text: str, source: str = "") -> list[Finding]:
    out: list[Finding] = []
    seen: set[tuple[str, str]] = set()
    for label, rx in _SECRET_PATTERNS:
        for m in rx.finditer(text or ""):
            value = m.group(m.lastindex or 0) if m.lastindex else m.group(0)
            key = (label, value)
            if key in seen:
                continue
            seen.add(key)
            out.append(Finding(kind=label, value=value, source=source))
    return out


def extract_sinks(text: str) -> dict[str, int]:
    return {name: len(rx.findall(text or "")) for name, rx in _SINKS if rx.search(text or "")}


def extract_sourcemaps(text: str) -> set[str]:
    out = set(_SOURCEMAP_RE.findall(text or ""))
    out |= set(_SOURCEURL_RE.findall(text or ""))
    return out


def analyze_text(text: str, source: str = "") -> dict:
    text = (text or "")[:_MAX_TEXT]
    urls = extract_urls(text)
    return {
        "source": source,
        "paths": sorted(extract_paths(text)),
        "urls": sorted(urls),
        "params": sorted(extract_params(text, urls)),
        "secrets": [f.__dict__ for f in extract_secrets(text, source)],
        "sinks": extract_sinks(text),
        "sourcemaps": sorted(extract_sourcemaps(text)),
    }


def _iter_files(root: Path):
    if root.is_file():
        yield root
    elif root.is_dir():
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix.lower() in (".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ""):
                yield p


def analyze_path(root: Path) -> dict:
    agg = {"sources": 0, "paths": set(), "urls": set(), "params": set(),
           "secrets": [], "sinks": {}, "sourcemaps": set()}
    for f in _iter_files(root):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        agg["sources"] += 1
        res = analyze_text(text, str(f))
        agg["paths"] |= set(res["paths"])
        agg["urls"] |= set(res["urls"])
        agg["params"] |= set(res["params"])
        agg["secrets"].extend(res["secrets"])
        for k, v in res["sinks"].items():
            agg["sinks"][k] = agg["sinks"].get(k, 0) + v
        agg["sourcemaps"] |= set(res["sourcemaps"])

    # dedupe secrets on (kind, value)
    uniq: dict[tuple[str, str], dict] = {}
    for s in agg["secrets"]:
        uniq[(s["kind"], s["value"])] = s
    return {
        "sources": agg["sources"],
        "paths": sorted(agg["paths"]),
        "urls": sorted(agg["urls"]),
        "params": sorted(agg["params"]),
        "secrets": sorted(uniq.values(), key=lambda d: (d["kind"], d["value"])),
        "sinks": dict(sorted(agg["sinks"].items())),
        "sourcemaps": sorted(agg["sourcemaps"]),
    }


def write_outputs(result: dict, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "endpoints.txt").write_text("\n".join(result["paths"]) + ("\n" if result["paths"] else ""), encoding="utf-8")
    (out_dir / "urls.txt").write_text("\n".join(result["urls"]) + ("\n" if result["urls"] else ""), encoding="utf-8")
    (out_dir / "params.txt").write_text("\n".join(result["params"]) + ("\n" if result["params"] else ""), encoding="utf-8")
    # Keep the historical filename — brain.py and recon_adapter.py read it.
    (out_dir / "potential_secrets.txt").write_text(
        "\n".join(f"{s['kind']}: {s['value']}  ({s['source']})" for s in result["secrets"])
        + ("\n" if result["secrets"] else ""), encoding="utf-8")
    (out_dir / "sourcemaps.txt").write_text(
        "\n".join(result["sourcemaps"]) + ("\n" if result["sourcemaps"] else ""), encoding="utf-8")
    (out_dir / "sinks.json").write_text(json.dumps(result["sinks"], indent=2) + "\n", encoding="utf-8")
    (out_dir / "analysis.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return {"out_dir": str(out_dir), "written": sorted(p.name for p in out_dir.iterdir())}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic offline JavaScript bundle analysis.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("analyze", help="analyze a JS file, directory, or - for stdin")
    pa.add_argument("path", help="file, directory, or - (stdin)")
    pa.add_argument("--out", default="", help="write endpoints/params/secrets/sinks/sourcemaps here")
    pa.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.path == "-":
        result = analyze_text(sys.stdin.read(), "<stdin>")
        result = {**result, "sources": 1}
    else:
        root = Path(args.path)
        if not root.exists():
            print(f"path not found: {root}", file=sys.stderr)
            return 2
        result = analyze_path(root)

    summary = {
        "sources": result["sources"],
        "endpoints": len(result["paths"]),
        "params": len(result["params"]),
        "secrets": len(result["secrets"]),
        "sinks": result["sinks"],
        "sourcemaps": len(result["sourcemaps"]),
    }
    if args.out:
        summary["output"] = write_outputs(result, Path(args.out))

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"sources:     {summary['sources']}")
    print(f"endpoints:   {summary['endpoints']}")
    print(f"params:      {summary['params']}")
    print(f"secrets:     {summary['secrets']}")
    print(f"sourcemaps:  {summary['sourcemaps']}")
    if summary["sinks"]:
        print("sinks:       " + ", ".join(f"{k}×{v}" for k, v in summary["sinks"].items()))
    if args.out:
        print(f"wrote:       {summary['output']['out_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
