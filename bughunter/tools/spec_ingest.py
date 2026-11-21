#!/usr/bin/env python3
"""Ingest an API specification into the attack surface.

Turns an OpenAPI 3.x / Swagger 2.0 / Postman v2 collection into a normalized,
classified list of endpoints so the API is tested from its *contract* instead of
only the handful of routes a crawler stumbles onto. Every declared endpoint
becomes a lead routed to a hunt-* skill (the same routing brain the lead board
uses), and the raw surface is written to recon/<target>/api/spec_endpoints.txt.

Why this exists: autonomous crawlers under-cover modern APIs (auth-gated,
versioned, behind feature flags). The spec is ground truth for what exists —
Shannon/Strix both drive API testing from the contract. This closes that gap
using the existing lead-board routing instead of a second engine.

LEAD-only: it parses a local spec and writes leads/enumerations. It never sends
a request to the target.

Usage:
  python3 bughunter/tools/spec_ingest.py spec.yaml --target api.example.com
  python3 bughunter/tools/spec_ingest.py spec.json --target api.example.com --ingest
  python3 bughunter/tools/spec_ingest.py postman.json --target api.example.com --json
  python3 bughunter/tools/spec_ingest.py spec.yaml --base https://api.example.com
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

_OBJECT_ID_RE = re.compile(
    r"(^|_|\b)(id|uid|uuid|guid|user|user_id|account|account_id|order|order_id|"
    r"invoice|doc|doc_id|file_id|record|profile|customer|cid|pid|num|no|key|slug)(_|$|\b)",
    re.I,
)
_URL_PARAM_NAMES = {
    "url", "uri", "dest", "destination", "domain", "site", "callback", "fetch",
    "load", "proxy", "feed", "host", "to", "out", "image_url", "imageurl",
    "continue_url", "return", "returnurl", "return_to", "redirect", "redirect_uri",
    "next", "goto", "success_url", "back",
}
_UPLOAD_HINTS = re.compile(r"upload|attachment|/files?/|avatar|/media|import|presign", re.I)
_PRIV_HINTS = re.compile(r"/(admin|manage|manage[sr]?|console|dashboard|actuator|debug|internal|staff|backoffice|operator|wp-admin)(/|$)", re.I)
_AUTH_HINTS = re.compile(r"(login|signin|sign-in|auth|sso|oauth|authorize|token|otp|2fa|mfa|reset|forgot|recover|verify)", re.I)
_LLM_HINTS = re.compile(r"/(chat|completions|assistant|copilot|llm|ai|embeddings|generate|conversation|messages)\b|/v1/(chat|messages)|/mcp\b", re.I)

_HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")
_PRIORITY_RANK = {"high": 0, "med": 1, "low": 2}
_URL_PARAM_PREFIXES = (
    "url", "uri", "callback", "redirect", "dest", "return", "next", "goto",
    "proxy", "fetch", "host", "domain", "site", "to", "out", "load", "feed",
)


def _snake(name: str) -> str:
    """userId -> user_id, callbackURL -> callback_url, X-Api-Key -> x_api_key."""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    return name.strip("_").lower()


def _is_url_param(name: str) -> bool:
    snake = _snake(name)
    return snake in _URL_PARAM_NAMES or any(
        snake == p or snake.startswith(p + "_") for p in _URL_PARAM_PREFIXES
    )


@dataclass
class Param:
    name: str
    location: str  # path | query | header | cookie | body
    required: bool = False
    type: str = ""
    format: str = ""


@dataclass
class Endpoint:
    method: str
    path: str
    base_url: str = ""
    operation_id: str = ""
    params: list[Param] = field(default_factory=list)
    has_body: bool = False
    security: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        base = (self.base_url or "").rstrip("/")
        path = self.path if self.path.startswith("/") else "/" + self.path
        return f"{base}{path}" if base else path

    def signal(self) -> str:
        bits = [b for b in (self.operation_id, ",".join(self.tags)) if b]
        return " · ".join(bits) or f"{self.method} {self.path}"


# ---------------------------------------------------------------------------
# Loading / parsing
# ---------------------------------------------------------------------------

def _load_structured(path: Path):
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError):
        pass
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - yaml is a test dep
        raise ValueError(
            "spec is not JSON and PyYAML is not installed "
            "(pip install pyyaml) to read YAML specs"
        ) from exc
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        raise ValueError(f"could not parse spec as JSON or YAML: {exc}") from exc


def detect_kind(spec) -> str | None:
    if not isinstance(spec, dict):
        return None
    if "openapi" in spec:
        return "openapi3"
    if "swagger" in spec:
        return "swagger2"
    info = spec.get("info")
    if isinstance(info, dict) and "schema" in info and "item" in spec:
        return "postman"
    if "item" in spec and "info" in spec:
        return "postman"
    return None


def _param_from_schema(name: str, location: str, raw: dict) -> Param:
    schema = raw.get("schema") if isinstance(raw.get("schema"), dict) else {}
    return Param(
        name=name,
        location=location,
        required=bool(raw.get("required", False)),
        type=str(raw.get("type") or schema.get("type") or ""),
        format=str(raw.get("format") or schema.get("format") or ""),
    )


def _swagger2_base(spec: dict) -> str:
    scheme = (spec.get("schemes") or ["https"])[0]
    host = spec.get("host") or ""
    base = spec.get("basePath") or ""
    return f"{scheme}://{host}{base}" if host else ""


def parse_openapi3(spec: dict, base_override: str = "") -> list[Endpoint]:
    servers = spec.get("servers") or []
    base = base_override or (servers[0].get("url", "") if servers else "")
    endpoints: list[Endpoint] = []
    for path, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        path_params = item.get("parameters") or []
        for method in _HTTP_METHODS:
            op = item.get(method)
            if not isinstance(op, dict):
                continue
            params = [_param_from_schema(p.get("name", ""), p.get("in", "query"), p)
                      for p in (*path_params, *(op.get("parameters") or []))
                      if isinstance(p, dict) and p.get("name")]
            has_body = bool(op.get("requestBody"))
            security = op.get("security", spec.get("security") or [])
            endpoints.append(Endpoint(
                method=method.upper(), path=path, base_url=base,
                operation_id=str(op.get("operationId") or ""),
                params=params, has_body=has_body,
                security=[list(s.keys())[0] if s else "" for s in security if isinstance(s, dict)],
                tags=[str(t) for t in (op.get("tags") or [])],
            ))
    return endpoints


def parse_swagger2(spec: dict, base_override: str = "") -> list[Endpoint]:
    base = base_override or _swagger2_base(spec)
    endpoints: list[Endpoint] = []
    for path, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        path_params = item.get("parameters") or []
        for method in _HTTP_METHODS:
            op = item.get(method)
            if not isinstance(op, dict):
                continue
            params = [_param_from_schema(p.get("name", ""), p.get("in", "query"), p)
                      for p in (*path_params, *(op.get("parameters") or []))
                      if isinstance(p, dict) and p.get("name")]
            body_params = op.get("parameters") or []
            has_body = any(isinstance(p, dict) and p.get("in") == "body" for p in body_params)
            security = op.get("security", spec.get("security") or [])
            endpoints.append(Endpoint(
                method=method.upper(), path=path, base_url=base,
                operation_id=str(op.get("operationId") or ""),
                params=params, has_body=has_body,
                security=[list(s.keys())[0] if s else "" for s in security if isinstance(s, dict)],
                tags=[str(t) for t in (op.get("tags") or [])],
            ))
    return endpoints


def _postman_url(raw) -> tuple[str, str, list[Param]]:
    """Return (base_url, path, query params) from a Postman url field."""
    if isinstance(raw, str):
        if "://" in raw:
            parts = urlsplit(raw)
            query = [Param(name=k, location="query") for k in parse_qs(parts.query)]
            return "", (parts.path or "/"), query
        return "", raw, []
    if not isinstance(raw, dict):
        return "", "", []
    segments = raw.get("path") or []
    path = "/" + "/".join(
        seg.get("value", "{}".format(seg.get("key", ""))) if isinstance(seg, dict) else str(seg)
        for seg in segments
    )
    query = [
        Param(name=str(q.get("key", "")), location="query", required=False)
        for q in (raw.get("query") or []) if isinstance(q, dict) and q.get("key")
    ]
    return "", path, query


def parse_postman(spec: dict, base_override: str = "") -> list[Endpoint]:
    endpoints: list[Endpoint] = []

    def walk(items, inherited_auth):
        for item in items or []:
            if not isinstance(item, dict):
                continue
            if "item" in item:
                walk(item["item"], item.get("auth") or inherited_auth)
                continue
            req = item.get("request")
            if not isinstance(req, dict):
                continue
            base, path, query = _postman_url(req.get("url"))
            method = str(req.get("method") or "GET").upper()
            auth = req.get("auth") or inherited_auth
            endpoints.append(Endpoint(
                method=method, path=path or "/",
                base_url=base_override or base,
                operation_id=str(item.get("name") or ""),
                params=query,
                has_body=bool(req.get("body")),
                security=["postman-auth"] if auth else [],
            ))

    walk(spec.get("item"), spec.get("auth"))
    return endpoints


def parse_spec(spec, base_override: str = "") -> tuple[str, list[Endpoint]]:
    kind = detect_kind(spec)
    if kind == "openapi3":
        return kind, parse_openapi3(spec, base_override)
    if kind == "swagger2":
        return kind, parse_swagger2(spec, base_override)
    if kind == "postman":
        return kind, parse_postman(spec, base_override)
    raise ValueError("unrecognized spec: expected OpenAPI 3.x, Swagger 2.0 or a Postman v2 collection")


# ---------------------------------------------------------------------------
# Classification — reuse the lead-board routing brain, then add spec signals
# ---------------------------------------------------------------------------

def _lead_board_routes(url: str) -> list[tuple[str, str, str, str]]:
    """Best-effort reuse of lead_board.route_observation (single routing brain)."""
    try:
        import lead_board
    except ImportError:
        return []
    try:
        return list(lead_board.route_observation(url, "url"))
    except Exception:
        return []


def classify(ep: Endpoint) -> list[dict]:
    """Return classified leads for one endpoint, highest priority first."""
    seen: dict[str, dict] = {}

    def add(skill: str, priority: str, label: str, why: str):
        cur = seen.get(skill)
        if cur is None or _PRIORITY_RANK.get(priority, 9) < _PRIORITY_RANK.get(cur["priority"], 9):
            seen[skill] = {"skill": skill, "priority": priority, "label": label, "why": why}

    # Reuse the URL routing brain on a representative URL (path + query names).
    sample = ep.path
    query_names = [p.name for p in ep.params if p.location == "query"]
    if query_names:
        sample += "?" + "&".join(f"{n}=" for n in query_names[:12])
    for skill, prio, label, why in _lead_board_routes(sample):
        add(skill, prio, label, why)

    path_l = ep.path.lower()
    # Path/query object references (the URL regex only catches numeric `id=1`).
    for p in ep.params:
        if p.location in ("path", "query") and _OBJECT_ID_RE.search(_snake(p.name)):
            add("hunt-idor", "high", "object reference",
                f"{p.location} param '{p.name}' references an object -> IDOR/BOLA: swap for another tenant's id")
        if _is_url_param(p.name):
            add("hunt-ssrf", "high", "URL-valued param",
                f"'{p.name}' looks server-fetched -> SSRF/IMDS")
            add("hunt-open-redirect", "med", "redirect param",
                f"'{p.name}' may drive a redirect -> open redirect / OAuth theft")

    if _UPLOAD_HINTS.search(path_l) or any(_UPLOAD_HINTS.search(p.name) for p in ep.params):
        add("hunt-file-upload", "high", "upload surface",
            "endpoint references uploads/files -> unrestricted upload / stored XSS / SSRF")
    if _PRIV_HINTS.search(path_l):
        add("hunt-auth-bypass", "high", "privileged path",
            "admin/internal path -> forced-browse / authz gap")
    if _AUTH_HINTS.search(path_l):
        add("hunt-oauth", "high", "auth flow",
            "login/token/otp/reset path -> authz-flow abuse, pre-ATO")
        add("hunt-ato", "high", "account-recovery flow",
            "recovery/verify path -> ATO via reset/OTP weakness")
    if _LLM_HINTS.search(path_l):
        add("hunt-llm-ai", "high", "AI/LLM endpoint",
            "chat/completions/mcp path -> prompt injection / tool abuse")

    # Undeclared auth on a mutating endpoint is an authorization-gap candidate.
    if ep.method in ("POST", "PUT", "PATCH", "DELETE") and not ep.security:
        add("hunt-api-misconfig", "med", "no security scheme declared",
            f"{ep.method} endpoint declares no auth -> check for missing authentication/authorization")

    if not seen:
        add("hunt-api-misconfig", "med", "API endpoint",
            "declared API endpoint -> auth gaps, mass-assignment, verb tampering")

    return sorted(seen.values(), key=lambda d: (_PRIORITY_RANK.get(d["priority"], 9), d["skill"]))


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def endpoint_lines(endpoints: list[Endpoint]) -> list[str]:
    lines = []
    for ep in endpoints:
        query = "&".join(f"{p.name}=" for p in ep.params if p.location == "query")
        url = ep.url + (f"?{query}" if query else "")
        lines.append(f"{ep.method} {url}")
    return sorted(set(lines))


def write_outputs(target: str, endpoints: list[Endpoint], recon_dir: str | os.PathLike | None,
                  classified: dict | None = None) -> dict:
    out_dir = Path(recon_dir) if recon_dir else Path("recon") / (target or "api")
    api_dir = out_dir / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    (api_dir / "spec_endpoints.txt").write_text("\n".join(endpoint_lines(endpoints)) + "\n", encoding="utf-8")
    artifact = {
        "target": target,
        "endpoint_count": len(endpoints),
        "endpoints": [asdict(ep) for ep in endpoints],
    }
    (api_dir / "spec_findings.json").write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"api_dir": str(api_dir), "written": len(endpoints)}


def ingest_to_board(target: str, classified: dict) -> tuple[int, int]:
    """Route classified leads to the persistent lead board. Returns (added, skipped)."""
    import lead_board
    added = skipped = 0
    for ep in classified.values():
        for lead in ep:
            existing = lead_board.add(
                target,
                skill=lead["skill"],
                evidence=lead["evidence"],
                signal=lead["label"],
                priority=lead["priority"],
            )
            if existing is None:
                skipped += 1
            else:
                added += 1
    return added, skipped


def build_classified(endpoints: list[Endpoint]) -> dict[str, list[dict]]:
    """Map endpoint line -> classification entries (with evidence attached)."""
    classified: dict[str, list[dict]] = {}
    for ep in endpoints:
        evidence = f"{ep.method} {ep.path}"
        entries = classify(ep)
        for e in entries:
            e["evidence"] = evidence[:300]
        classified[f"{ep.method} {ep.path}"] = entries
    return classified


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Ingest an OpenAPI/Swagger/Postman spec into the attack surface.")
    ap.add_argument("spec", help="path to the spec file (JSON or YAML)")
    ap.add_argument("--target", default="", help="target name for output dir (default: derived from spec)")
    ap.add_argument("--base", default="", help="override base URL")
    ap.add_argument("--recon-dir", default="", help="output dir (default: recon/<target>)")
    ap.add_argument("--ingest", action="store_true", help="route distinct leads to the persistent lead board")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    path = Path(args.spec)
    if not path.is_file():
        print(f"spec not found: {path}", file=sys.stderr)
        return 2
    try:
        spec = _load_structured(path)
        kind, endpoints = parse_spec(spec, args.base)
    except ValueError as exc:
        print(f"invalid spec: {exc}", file=sys.stderr)
        return 1

    target = args.target or _derive_target(spec, endpoints, path)
    classified = build_classified(endpoints)
    outputs = write_outputs(target, endpoints, args.recon_dir or None, classified)

    lead_count = sum(len(v) for v in classified.values())
    summary = {
        "target": target,
        "spec_kind": kind,
        "endpoints": len(endpoints),
        "leads": lead_count,
        "api_dir": outputs["api_dir"],
        "top_skills": _skill_histogram(classified),
    }
    if args.ingest:
        added, skipped = ingest_to_board(target, {
            k: [e for e in v] for k, v in classified.items()
        })
        summary.update({"board_added": added, "board_skipped": skipped})

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"spec:       {kind}")
    print(f"target:     {target}")
    print(f"endpoints:  {len(endpoints)}")
    print(f"leads:      {lead_count}  -> {outputs['api_dir']}/spec_endpoints.txt")
    if args.ingest:
        print(f"board:      +{summary['board_added']} lead(s) ({summary['board_skipped']} already present)")
    print("\nTop routing:")
    for skill, n in list(summary["top_skills"].items())[:10]:
        print(f"  {n:>3}  {skill}")
    return 0


def _derive_target(spec, endpoints, path: Path) -> str:
    if endpoints and endpoints[0].base_url:
        host = re.sub(r"^https?://", "", endpoints[0].base_url).split("/")[0].split(":")[0]
        if host:
            return host
    if isinstance(spec, dict):
        host = (spec.get("host") or "").split(":")[0]
        if host:
            return host
    return path.stem


def _skill_histogram(classified: dict[str, list[dict]]) -> dict[str, int]:
    hist: dict[str, int] = {}
    for entries in classified.values():
        for e in entries:
            hist[e["skill"]] = hist.get(e["skill"], 0) + 1
    return dict(sorted(hist.items(), key=lambda kv: (-kv[1], kv[0])))


if __name__ == "__main__":
    raise SystemExit(main())
