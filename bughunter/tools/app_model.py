#!/usr/bin/env python3
"""App model builder — one structured map of the target, built BEFORE hunting.

The 2026 lesson (Pathan, Pearlstein): agents that model the app first
(endpoints → auth → identities → object references) find more real bugs than
agents that fire payloads blind. This builds a deduplicated `app-model/1` from
whatever recon you already have — URL lists, JS bundles, OpenAPI/Postman specs —
and marks the object references that make IDOR/BOLA/GraphQL-IDOR testable.

It never touches the network. It only reads local recon artifacts and writes a
JSON model other tools can consume:

    python3 -m tools.app_model build --target acme.com --recon-dir recon/acme.com \
        --spec openapi.json --out recon/acme.com/app_model.json
    python3 -m tools.app_model build --target acme.com --urls urls.txt --json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs

SCHEMA = "app-model/1"

_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
_HEX = re.compile(r"^[0-9a-fA-F]{8,}$")
_NUM = re.compile(r"^\d+$")

# Param names that usually address an object/tenant -> the IDOR surface.
_OBJECT_TOKEN = re.compile(
    r"(^|_)(id|uid|pid|uuid|guid|user|account|acct|order|invoice|tenant|org|"
    r"project|team|workspace|email|username|handle|slug|file|doc|report|card)$",
    re.IGNORECASE,
)

_METHOD_RE = re.compile(r'\.(get|post|put|patch|delete)\(\s*["\'`]([^"\'`]+)', re.IGNORECASE)
_FETCH_RE = re.compile(r'fetch\(\s*["\'`]([^"\'`]+)')
_PATH_RE = re.compile(r'["\'`](/[A-Za-z0-9_\-./{}:]{2,})["\'`]')
_URL_RE = re.compile(r"https?://[^\s\"'<>)]+")


try:
    from tools.lead_board import _is_content_page
except Exception:  # pragma: no cover
    def _is_content_page(_u):
        return False

def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_path(path: str) -> str:
    """Collapse concrete ids to placeholders so one endpoint dedups to one key."""
    path = path.strip()
    if not path:
        return "/"
    if not path.startswith("/"):
        path = "/" + path
    # strip query/fragment for the canonical path
    path = path.split("?", 1)[0].split("#", 1)[0]
    out = []
    for seg in path.split("/"):
        if not seg:
            out.append("")
        elif seg.startswith(":"):
            out.append("{id}")
        elif seg.startswith("{") and seg.endswith("}"):
            out.append(seg)
        elif _NUM.match(seg):
            out.append("{id}")
        elif _UUID.match(seg):
            out.append("{uuid}")
        elif _HEX.match(seg) and len(seg) >= 12:
            out.append("{hash}")
        else:
            out.append(seg)
    return "/".join(out) or "/"


def endpoint_key(method: str, path: str) -> str:
    return f"{method.upper()} {normalize_path(path)}"


def is_object_param(name: str) -> bool:
    return bool(_OBJECT_TOKEN.search(name or ""))


def _params_from_query(url: str) -> list[dict]:
    q = parse_qs(urlparse(url).query, keep_blank_values=True)
    return [{"name": k, "in": "query", "object_ref": is_object_param(k)} for k in q]


def _add(endpoints: dict, method: str, path: str, source: str,
         params: list[dict] | None = None, base_url: str = "") -> None:
    if not path:
        return
    key = endpoint_key(method, path)
    ep = endpoints.setdefault(key, {
        "key": key, "method": method.upper(), "path": normalize_path(path),
        "base_url": base_url, "params": [], "object_refs": [], "sources": [],
    })
    if source not in ep["sources"]:
        ep["sources"].append(source)
    seen = {(p["name"], p["in"]) for p in ep["params"]}
    for p in params or []:
        if (p["name"], p["in"]) not in seen:
            ep["params"].append(p)
            seen.add((p["name"], p["in"]))
    # path placeholders are object refs too
    for seg in ep["path"].split("/"):
        if seg.startswith("{") and seg != "{hash}":
            if seg not in ep["object_refs"]:
                ep["object_refs"].append(seg)
    for p in ep["params"]:
        if p.get("object_ref") and p["name"] not in ep["object_refs"]:
            ep["object_refs"].append(p["name"])


def extract_from_urls(urls: list[str], endpoints: dict | None = None) -> dict:
    endpoints = endpoints if endpoints is not None else {}
    for raw in urls:
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        if _is_content_page(raw):
            continue  # docs/blog/marketing are content, not an IDOR/object surface
        if not raw.startswith("http"):
            _add(endpoints, "GET", raw, "url")
            continue
        u = urlparse(raw)
        _add(endpoints, "GET", u.path or "/", "url", _params_from_query(raw),
             base_url=f"{u.scheme}://{u.netloc}")
    return endpoints


def extract_from_js(text: str, source: str = "js", endpoints: dict | None = None) -> dict:
    endpoints = endpoints if endpoints is not None else {}
    for m in _METHOD_RE.finditer(text):
        _add(endpoints, m.group(1), m.group(2), source)
    for m in _FETCH_RE.finditer(text):
        _add(endpoints, "GET", m.group(1), source)
    for m in _PATH_RE.finditer(text):
        p = m.group(1)
        if p.startswith("/") and len(p) > 2 and not p.startswith("//"):
            _add(endpoints, "GET", p, source)
    return endpoints


def extract_from_spec(path: str, endpoints: dict | None = None) -> dict:
    endpoints = endpoints if endpoints is not None else {}
    try:
        from tools.spec_ingest import parse_spec
        spec = json.loads(open(path, encoding="utf-8").read())
        _kind, eps = parse_spec(spec)
    except Exception:  # noqa: BLE001 - best-effort; non-JSON specs are skipped
        return endpoints
    for ep in eps:
        params = [{"name": p.name, "in": getattr(p, "location", "query"),
                   "object_ref": is_object_param(p.name)} for p in getattr(ep, "params", [])]
        _add(endpoints, getattr(ep, "method", "GET"), getattr(ep, "path", ""),
             f"spec:{os.path.basename(path)}", params, getattr(ep, "base_url", ""))
    return endpoints


def _gather_recon(recon_dir: str) -> tuple[list[str], list[str]]:
    urls: list[str] = []
    js_files: list[str] = []
    for path in glob.glob(os.path.join(recon_dir, "**", "*"), recursive=True):
        if not os.path.isfile(path):
            continue
        low = path.lower()
        try:
            if low.endswith((".js", ".mjs", ".jsx", ".ts")):
                js_files.append(path)
            elif low.endswith((".txt", ".lst", ".csv")):
                for line in open(path, encoding="utf-8", errors="ignore"):
                    line = line.strip()
                    if line:
                        urls.extend(_URL_RE.findall(line) or ([line] if "/" in line else []))
        except OSError:
            continue
    return urls, js_files


def build(target: str, *, urls: list[str] | None = None,
          js_texts: dict[str, str] | None = None,
          specs: list[str] | None = None,
          recon_dir: str | None = None) -> dict:
    all_urls = list(urls or [])
    js_files: list[str] = []
    if recon_dir:
        r_urls, r_js = _gather_recon(recon_dir)
        all_urls += r_urls
        js_files += r_js

    endpoints: dict = {}
    extract_from_urls(all_urls, endpoints)
    for source, text in (js_texts or {}).items():
        extract_from_js(text, source, endpoints)
    for jf in js_files:
        try:
            extract_from_js(open(jf, encoding="utf-8", errors="ignore").read(),
                            os.path.basename(jf), endpoints)
        except OSError:
            continue
    for sp in specs or []:
        extract_from_spec(sp, endpoints)

    eps = sorted(endpoints.values(), key=lambda e: e["key"])

    hosts = sorted({e["base_url"].split("//")[-1] for e in eps if e.get("base_url")})
    mechanisms = []
    if any(re.search(r"auth|login|token|oauth|session", e["path"], re.I) for e in eps):
        mechanisms.append("auth-endpoints")
    object_eps = [e["key"] for e in eps if e["object_refs"]]
    object_objs: dict = {}
    for e in eps:
        for ref in e["object_refs"]:
            object_objs.setdefault(ref, []).append(e["key"])

    return {
        "schema": SCHEMA,
        "target": target,
        "generated_at": _now(),
        "hosts": hosts,
        "auth": {"mechanisms": mechanisms},
        "endpoints": eps,
        "identities": [],
        "objects": [{"ref": k, "endpoints": v} for k, v in sorted(object_objs.items())],
        "stats": {
            "endpoints": len(eps),
            "object_endpoints": len(object_eps),
            "hosts": len(hosts),
        },
    }


def write(model: dict, path: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(model, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build a deduplicated app model from recon")
    ap.add_argument("--target", required=True)
    ap.add_argument("--recon-dir")
    ap.add_argument("--urls", help="file with one URL/path per line")
    ap.add_argument("--spec", action="append", default=[], help="OpenAPI/Postman JSON (repeatable)")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    urls: list[str] = []
    if args.urls:
        urls = [ln.strip() for ln in open(args.urls, encoding="utf-8", errors="ignore")
                if ln.strip()]

    model = build(args.target, urls=urls, specs=args.spec, recon_dir=args.recon_dir)
    if args.out:
        write(model, args.out)
    if args.json or not args.out:
        print(json.dumps(model, indent=2, sort_keys=True))
    else:
        s = model["stats"]
        print(f"[+] app model: {s['endpoints']} endpoints, "
              f"{s['object_endpoints']} with object refs, {s['hosts']} hosts -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
