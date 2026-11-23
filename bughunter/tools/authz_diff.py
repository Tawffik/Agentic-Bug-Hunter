#!/usr/bin/env python3
"""authz_diff.py — two-identity authorization differential engine (IDOR/BOLA).

The #1 paid web2 bug class needs two authenticated identities and a controlled
comparison: take a request that worked for identity A (the object owner), replay
it as identity B (the attacker), and compare against an anonymous control.
This tool automates that loop over recon endpoints or a HAR capture and emits
LEAD-only results plus an optional deterministic confirmation through the
existing IDOR verifier.

What it does NOT do:
  * it never mutates object identifiers to guess other users' ids,
  * it never follows redirects (single-hop, SSRF-guarded),
  * it never persists request headers or response bodies (redacted metadata
    only), and
  * it never calls a lead "confirmed" on similarity alone. Only the IDOR
    verifier's cross-user marker check can produce a CONFIRMED result.

Usage:
  python3 bughunter/tools/authz_diff.py \
      --recon-dir recon/target.com \
      --headers-a .private/a.json --headers-b .private/b.json \
      --victim-marker alice@example.test --scope target.com --confirm

  python3 bughunter/tools/authz_diff.py --har capture.har \
      --headers-b .private/b.json --scope target.com
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from tools.verifiers.base import fetch  # noqa: E402
from memory.redaction import redact_obj  # noqa: E402

HIGH_SIM = 0.95
MEDIUM_SIM = 0.85
PUBLIC_SIM = 0.90
MIN_BODY = 16
SIM_CHAR_CAP = 12000

_STATIC_EXT = re.compile(
    r"\.(?:png|jpe?g|gif|svg|ico|webp|woff2?|ttf|eot|css|less|scss|mp4|webm|"
    r"pdf|zip|map|txt|xml|rss|json)$",
    re.I,
)
_OBJECT_KEY = re.compile(
    r"(?i)(?:^|_)(id|uid|uuid|guid|user|account|order|invoice|report|item|"
    r"object|resource|tenant|org|team|project|doc|file|payment|transaction|"
    r"customer|member|profile|message|ticket)(?:s|_id)?(?:$|_)"
)
_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
_HEX_RE = re.compile(r"^[0-9a-f]{16,}$", re.I)
_NUM_RE = re.compile(r"^\d{1,15}$")
_B64ISH_RE = re.compile(r"^[A-Za-z0-9+/=_-]{16,}$")

_DENY_STATUS = {401, 403, 404, 410, 451}
_DENY_TEXT = (
    "sign in", "log in", "login required", "unauthorized", "unauthorised",
    "permission denied", "access denied", "not authorized", "not authorised",
    "forbidden", "authentication required",
)
_VOLATILE_KEYS = {
    "timestamp", "ts", "time", "date", "now", "nonce", "request_id", "requestid",
    "trace_id", "traceid", "correlation_id", "expires", "expiry", "exp",
    "csrf", "csrf_token", "xsrf", "server_time", "elapsed", "duration",
}
_HEADER_SKIP = {"host", "content-length", "connection", "transfer-encoding", "accept-encoding"}


@dataclass
class Identity:
    name: str
    headers: dict[str, str] = field(default_factory=dict)

    def redacted(self) -> dict:
        return {"name": self.name, "headers": list(self.headers)}


@dataclass
class Probe:
    status: int | None
    body: bytes
    content_type: str
    length: int
    error: str | None = None

    def text(self) -> str:
        return self.body.decode("utf-8", "replace")


@dataclass
class Case:
    url: str
    object_ref: bool
    verdict: str
    confidence: str
    reason: str
    similarity: float = 0.0
    schema_similarity: float = 0.0
    status: dict = field(default_factory=dict)
    length: dict = field(default_factory=dict)
    marker_match: bool = False
    anon_leak: bool = False
    verifier: dict | None = None

    def to_dict(self) -> dict:
        return dict(self.__dict__)


def _content_type(headers: dict) -> str:
    for key, value in headers.items():
        if key.lower() == "content-type":
            return str(value).split(";")[0].strip().lower()
    return ""


def _probe(exchange, body: bytes) -> Probe:
    return Probe(
        status=exchange.status,
        body=body,
        content_type=_content_type(exchange.response_headers or {}),
        length=len(body),
        error=exchange.note if exchange.status is None else None,
    )


def _is_denied(p: Probe) -> bool:
    if p.status in _DENY_STATUS:
        return True
    if p.status is None:
        return True
    if p.status == 200 and 0 < p.length < 2000 and "html" in p.content_type:
        low = p.text()[:1500].lower()
        return any(marker in low for marker in _DENY_TEXT)
    return False


def _is_ok(p: Probe) -> bool:
    return p.status is not None and 200 <= p.status < 300 and p.length >= MIN_BODY and not _is_denied(p)


def _looks_like_object(value: str) -> bool:
    value = value.strip()
    if not value or len(value) > 256:
        return False
    if _NUM_RE.match(value):
        return True
    if _UUID_RE.match(value) or _HEX_RE.match(value):
        return True
    if _B64ISH_RE.match(value) and any(c.isdigit() for c in value) and any(c.isalpha() for c in value):
        return True
    return False


def has_object_ref(url: str) -> bool:
    """True when the URL carries a plausible object identifier."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    for key, values in parse_qs(parsed.query, keep_blank_values=True).items():
        if _OBJECT_KEY.search(key) and any(_looks_like_object(v) for v in values):
            return True
    for segment in parsed.path.split("/"):
        if _looks_like_object(segment):
            return True
    return False


def _json_shape(obj, prefix: str = "", out: set | None = None) -> set:
    if out is None:
        out = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            out.add(path)
            _json_shape(value, path, out)
    elif isinstance(obj, list):
        for value in obj[:5]:
            _json_shape(value, prefix + "[]", out)
    return out


def _canonical_json(obj):
    if isinstance(obj, dict):
        return {
            str(k): ("<volatile>" if str(k).lower() in _VOLATILE_KEYS else _canonical_json(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_canonical_json(v) for v in obj[:20]]
    return obj


def _ratio(a: str, b: str) -> float:
    """Similarity with a token fallback so huge bodies stay near-linear."""
    if max(len(a), len(b)) > 6000:
        ta = set(re.findall(r"[A-Za-z0-9_]+", a.lower()))
        tb = set(re.findall(r"[A-Za-z0-9_]+", b.lower()))
        union = ta | tb
        return len(ta & tb) / len(union) if union else 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def _text_norm(text: str) -> str:
    text = text[:SIM_CHAR_CAP]
    text = re.sub(r"\s+", " ", text).strip().lower()
    text = re.sub(r"\b[0-9a-f]{8}-[0-9a-f-]{27,}\b", "<uuid>", text)
    text = re.sub(r"\b[0-9a-f]{24,}\b", "<hex>", text)
    text = re.sub(r"\b\d{6,}\b", "<num>", text)
    return text


def similarity(a: Probe, b: Probe) -> tuple[float, float]:
    """Return (value_similarity, schema_similarity) in [0,1]."""
    a_text, b_text = a.text(), b.text()
    try:
        a_json, b_json = json.loads(a_text), json.loads(b_text)
        schema_a, schema_b = _json_shape(a_json), _json_shape(b_json)
        union = schema_a | schema_b
        schema_sim = len(schema_a & schema_b) / len(union) if union else 0.0
        a_can = json.dumps(_canonical_json(a_json), sort_keys=True, ensure_ascii=False)[:SIM_CHAR_CAP]
        b_can = json.dumps(_canonical_json(b_json), sort_keys=True, ensure_ascii=False)[:SIM_CHAR_CAP]
        return _ratio(a_can, b_can), schema_sim
    except (ValueError, TypeError, RecursionError):
        pass
    return _ratio(_text_norm(a_text), _text_norm(b_text)), 0.0


def classify(
    *,
    url: str,
    a: Probe,
    b: Probe,
    anon: Probe | None,
    marker_a: str = "",
    marker_b: str = "",
    include_html: bool = False,
) -> Case:
    """Classify one A/B/anon triple into a lead verdict.

    Verdicts:
      CROSS_USER_MARKER          B's response contains A's unique marker
      IDENTICAL_ACROSS_IDENTITIES near-identical bodies on an object-bearing URL
      SAME_SCHEMA_DIFFERENT_DATA ambiguous same-shape/different-values result
      PUBLIC                     anonymous control also succeeds identically
      ENFORCED                   B (or A baseline) is denied
      DISTINCT_PER_USER          each identity sees its own marker (negative)
      UNKNOWN                    error / undetermined
    """
    status = {"a": a.status, "b": b.status, "anon": anon.status if anon else None}
    length = {"a": a.length, "b": b.length, "anon": anon.length if anon else None}
    obj_ref = has_object_ref(url)
    base = dict(url=url, object_ref=obj_ref, status=status, length=length)

    if a.error or a.status is None:
        return Case(verdict="UNKNOWN", confidence="none", reason=f"A request failed: {a.error}", **base)
    if _is_denied(a):
        return Case(verdict="UNKNOWN", confidence="none",
                    reason="identity A is denied — capture a request A legitimately owns", **base)
    if not _is_ok(a):
        return Case(verdict="UNKNOWN", confidence="none",
                    reason=f"A response is not a substantive success (status {a.status}, {a.length}B)", **base)

    a_text, b_text, anon_text = a.text(), b.text(), anon.text() if anon else ""
    sim_ab, schema_ab = similarity(a, b)

    if marker_a and marker_a in b_text:
        if anon and marker_a in anon_text:
            return Case(verdict="PUBLIC_EXPOSURE", confidence="high", marker_match=True,
                        anon_leak=True, similarity=sim_ab, schema_similarity=schema_ab,
                        reason="A's marker is also returned anonymously — exposure, not identity differential",
                        **base)
        return Case(verdict="CROSS_USER_MARKER", confidence="high", marker_match=True,
                    similarity=sim_ab, schema_similarity=schema_ab,
                    reason="identity B received identity A's unique marker", **base)

    if anon and _is_ok(anon):
        sim_an, _ = similarity(a, anon)
        ratio = (anon.length + 1) / (a.length + 1)
        if sim_an >= PUBLIC_SIM and 0.6 <= ratio <= 1.6:
            return Case(verdict="PUBLIC", confidence="none", similarity=sim_an,
                        reason="anonymous control receives the same response — public resource", **base)

    if _is_denied(b):
        return Case(verdict="ENFORCED", confidence="none", similarity=sim_ab,
                    schema_similarity=schema_ab,
                    reason=f"identity B denied (status {b.status})", **base)

    if not _is_ok(b):
        return Case(verdict="UNKNOWN", confidence="none", similarity=sim_ab,
                    reason=f"B response is not substantive (status {b.status}, {b.length}B)", **base)

    ctype = b.content_type or a.content_type
    if "html" in ctype and not include_html:
        return Case(verdict="SKIPPED", confidence="none", similarity=sim_ab,
                    reason="HTML body skipped by default (use --include-html)", **base)

    if marker_a and marker_b and marker_a in a_text and marker_b in b_text:
        return Case(verdict="DISTINCT_PER_USER", confidence="none", similarity=sim_ab,
                    schema_similarity=schema_ab,
                    reason="each identity sees its own marker — per-user isolation holds", **base)

    sim_an = 0.0
    if anon:
        sim_an, _ = similarity(a, anon)

    if obj_ref and sim_ab >= HIGH_SIM and schema_ab >= 0.8 and sim_an < PUBLIC_SIM:
        confidence = "high" if (sim_ab >= 0.98 and anon is not None) else "medium"
        reason = "two identities receive near-identical substantive responses for the same object URL"
        if anon is None:
            reason += " (no anonymous control was run)"
        return Case(verdict="IDENTICAL_ACROSS_IDENTITIES", confidence=confidence,
                    similarity=sim_ab, schema_similarity=schema_ab,
                    reason=reason, **base)
    if obj_ref and sim_ab >= MEDIUM_SIM and (schema_ab >= 0.9 or schema_ab == 0.0):
        return Case(verdict="SAME_SCHEMA_DIFFERENT_DATA", confidence="medium",
                    similarity=sim_ab, schema_similarity=schema_ab,
                    reason="same object URL returns substantive data to both identities",
                    **base)
    return Case(verdict="DISTINCT", confidence="none", similarity=sim_ab,
                schema_similarity=schema_ab, reason="responses differ materially", **base)


def parse_headers_text(text: str) -> dict[str, str]:
    """Parse a header file: JSON object, Playwright storage-state, or `K: V` lines."""
    text = text.strip()
    if not text:
        raise ValueError("empty header file")
    if text.startswith("{"):
        data = json.loads(text)
        if isinstance(data.get("cookies"), list):
            cookie_parts = [
                f"{c.get('name')}={c.get('value')}"
                for c in data["cookies"]
                if c.get("name") and c.get("value") is not None
            ]
            if not cookie_parts:
                raise ValueError(
                    "storage-state has no cookies; localStorage-only sessions cannot be "
                    "replayed as a Cookie header"
                )
            return {"Cookie": "; ".join(cookie_parts)}
        if isinstance(data.get("headers"), dict):
            data = data["headers"]
        if not isinstance(data, dict):
            raise ValueError("JSON header file must be an object")
        return {str(k): str(v) for k, v in data.items()}
    headers: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            name, value = line.split(":", 1)
            headers[name.strip()] = value.strip()
        elif "=" in line:
            headers["Cookie"] = line
        else:
            raise ValueError(f"invalid header line: {line[:60]!r}")
    if not headers:
        raise ValueError("no headers parsed")
    return headers


def load_identity(name: str, path: str | None, cookie: str = "", bearer: str = "") -> Identity:
    headers: dict[str, str] = {}
    if path:
        headers.update(parse_headers_text(Path(path).read_text(encoding="utf-8")))
    if cookie:
        headers["Cookie"] = cookie
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    headers = {k: v for k, v in headers.items() if k.lower() not in _HEADER_SKIP}
    return Identity(name=name, headers=headers)


def _absolute_urls(lines, scope_checker=None) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in lines:
        url = str(raw).strip()
        if not url or url.startswith(("#", "//")):
            continue
        if not url.lower().startswith(("http://", "https://")):
            continue
        parsed = urlparse(url)
        if not parsed.hostname or _STATIC_EXT.search(parsed.path or ""):
            continue
        if scope_checker is not None and not scope_checker.is_in_scope(url):
            continue
        if url in seen:
            continue
        seen.add(url)
        out.append(url)
    return out


def urls_from_recon(recon_dir: str | Path, scope_checker=None) -> list[str]:
    recon = Path(recon_dir)
    candidates = [
        recon / "urls" / "with_params.txt",
        recon / "urls" / "api_endpoints.txt",
        recon / "js" / "endpoints.txt",
        recon / "urls" / "all.txt",
    ]
    lines: list[str] = []
    for path in candidates:
        if path.is_file():
            lines.extend(path.read_text(encoding="utf-8", errors="replace").splitlines())
    return _absolute_urls(lines, scope_checker)


def urls_from_har(path: str | Path, methods: tuple[str, ...] = ("GET",), scope_checker=None) -> list[str]:
    data = json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    lines: list[str] = []
    for entry in data.get("log", {}).get("entries", []):
        request = entry.get("request") or {}
        if str(request.get("method", "GET")).upper() not in methods:
            continue
        if request.get("url"):
            lines.append(request["url"])
    return _absolute_urls(lines, scope_checker)


class Scanner:
    def __init__(self, *, identity_a: Identity | None, identity_b: Identity,
                 marker_a: str = "", marker_b: str = "", anon: bool = True,
                 include_html: bool = False, timeout: float = 15.0,
                 delay: float = 0.1, scope_checker=None, confirm: bool = False):
        self.identity_a = identity_a
        self.identity_b = identity_b
        self.marker_a = marker_a
        self.marker_b = marker_b
        self.anon = anon
        self.include_html = include_html
        self.timeout = timeout
        self.delay = delay
        self.scope_checker = scope_checker
        self.confirm = confirm
        self._site = None
        if scope_checker is not None:
            self._site = getattr(scope_checker, "domains", None)

    def _request(self, url: str, headers: dict) -> Probe:
        exchange, body = fetch(url, headers=headers, timeout=self.timeout,
                               scope_checker=self.scope_checker, note="authz-diff")
        return _probe(exchange, body)

    def scan(self, url: str) -> Case:
        a = self._request(url, self.identity_a.headers) if self.identity_a else None
        if a is None:
            a = self._request(url, {})
        b = self._request(url, self.identity_b.headers)
        anon = self._request(url, {}) if self.anon else None
        if self.delay:
            time.sleep(self.delay)
        case = classify(url=url, a=a, b=b, anon=anon,
                        marker_a=self.marker_a, marker_b=self.marker_b,
                        include_html=self.include_html)
        if self.confirm and case.verdict == "CROSS_USER_MARKER" and self.marker_a:
            case.verifier = self._confirm(url)
        return case

    def _confirm(self, url: str) -> dict:
        from tools.validate_core import verify_finding_programmatic

        finding = {
            "vuln_class": "idor",
            "victim_object_url": url,
            "attacker_headers": self.identity_b.headers,
            "victim_marker": self.marker_a,
            "target": (self._site or ["authz-diff"])[0],
        }
        result = verify_finding_programmatic(
            finding, scope_checker=self.scope_checker, log_research=False
        )
        return {
            "status": result.get("status"),
            "technically_confirmed": result.get("technically_confirmed"),
            "reason": (result.get("rejection_reasons") or [None])[0],
            "oracle": (result.get("verifier") or {}).get("oracle"),
        }


def _redacted_case(case: Case) -> dict:
    data = case.to_dict()
    return redact_obj(data)


def _write_results(out_dir: str, cases: list[Case], meta: dict) -> str:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    jsonl = path / f"authz-diff-{stamp}.jsonl"
    with jsonl.open("w", encoding="utf-8") as fh:
        for case in cases:
            fh.write(json.dumps(_redacted_case(case), sort_keys=True) + "\n")
    summary = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tested": len(cases),
        "counts": {},
        "results_file": str(jsonl),
        **meta,
    }
    for case in cases:
        summary["counts"][case.verdict] = summary["counts"].get(case.verdict, 0) + 1
    (path / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return str(jsonl)


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Two-identity authorization differential scanner (LEAD-only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--urls", help="file of absolute URLs to test")
    src.add_argument("--recon-dir", help="recon directory (reads urls/ + js/endpoints.txt)")
    src.add_argument("--har", help="HAR capture of identity A's authenticated traffic")
    ap.add_argument("--headers-a", help="identity A headers file (json / storage-state / k: v)")
    ap.add_argument("--headers-b", required=True, help="identity B (attacker) headers file")
    ap.add_argument("--cookie-a", default="", help="identity A Cookie header value")
    ap.add_argument("--cookie-b", default="", help="identity B Cookie header value")
    ap.add_argument("--victim-marker", default="", help="unique value belonging to A (e.g. A's email)")
    ap.add_argument("--attacker-marker", default="", help="unique value belonging to B (FP control)")
    ap.add_argument("--scope", action="append", default=[],
                    help="in-scope pattern (host, *.host, host:port, CIDR). Required for live traffic.")
    ap.add_argument("--scope-exclude", action="append", default=[])
    ap.add_argument("--methods", default="GET", help="HAR methods to ingest (default GET)")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--max-urls", type=int, default=500)
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--delay", type=float, default=0.1)
    ap.add_argument("--include-html", action="store_true", help="also test text/html endpoints")
    ap.add_argument("--no-anon", action="store_true", help="skip the anonymous control")
    ap.add_argument("--confirm", action="store_true",
                    help="run the deterministic IDOR verifier on cross-user-marker leads")
    ap.add_argument("--out", default="", help="output directory (default findings/<scope>/authz)")
    ap.add_argument("--json", action="store_true", help="print JSONL to stdout")
    return ap


def _main(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)

    scope_patterns = []
    for chunk in args.scope:
        scope_patterns.extend(p.strip() for p in chunk.split(",") if p.strip())
    if not scope_patterns:
        print("error: --scope is required for live authorization testing", file=sys.stderr)
        return 2

    from tools.scope_checker import ScopeChecker

    try:
        scope = ScopeChecker(scope_patterns, excluded_domains=args.scope_exclude or None)
    except Exception as exc:  # noqa: BLE001
        print(f"error: unsafe scope configuration: {exc}", file=sys.stderr)
        return 2

    try:
        identity_b = load_identity("b", args.headers_b, cookie=args.cookie_b)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: identity B: {exc}", file=sys.stderr)
        return 2
    if not identity_b.headers:
        print("error: identity B has no headers", file=sys.stderr)
        return 2
    identity_a = None
    if args.headers_a or args.cookie_a:
        try:
            identity_a = load_identity("a", args.headers_a, cookie=args.cookie_a)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: identity A: {exc}", file=sys.stderr)
            return 2

    if args.urls:
        lines = Path(args.urls).read_text(encoding="utf-8", errors="replace").splitlines()
        urls = _absolute_urls(lines, scope)
    elif args.recon_dir:
        urls = urls_from_recon(args.recon_dir, scope)
    else:
        methods = tuple(m.strip().upper() for m in args.methods.split(",") if m.strip())
        try:
            urls = urls_from_har(args.har, methods=methods, scope_checker=scope)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: HAR: {exc}", file=sys.stderr)
            return 2

    urls = urls[: max(1, args.max_urls)]
    if not urls:
        print("error: no in-scope absolute URLs found", file=sys.stderr)
        return 2

    scanner = Scanner(
        identity_a=identity_a, identity_b=identity_b,
        marker_a=args.victim_marker, marker_b=args.attacker_marker,
        anon=not args.no_anon, include_html=args.include_html,
        timeout=args.timeout, delay=args.delay, scope_checker=scope,
        confirm=args.confirm,
    )

    cases: list[Case] = []
    with ThreadPoolExecutor(max_workers=max(1, args.threads)) as pool:
        futures = {pool.submit(scanner.scan, url): url for url in urls}
        for idx, future in enumerate(as_completed(futures), 1):
            url = futures[future]
            try:
                case = future.result()
            except Exception as exc:  # noqa: BLE001 - one bad URL must not stop the sweep
                case = Case(url=url, object_ref=False, verdict="UNKNOWN", confidence="none",
                            reason=f"{type(exc).__name__}: {exc}")
            cases.append(case)
            if args.json:
                print(json.dumps(_redacted_case(case), sort_keys=True))
            elif case.verdict in {"CROSS_USER_MARKER", "IDENTICAL_ACROSS_IDENTITIES",
                                  "SAME_SCHEMA_DIFFERENT_DATA", "PUBLIC_EXPOSURE"}:
                print(f"[{case.confidence.upper()}] {case.verdict} {url} "
                      f"(sim={case.similarity:.2f}, status={case.status})", flush=True)
            if idx % 25 == 0:
                print(f"  ... {idx}/{len(urls)} tested", file=sys.stderr, flush=True)

    meta = {
        "identity_a": identity_a.redacted() if identity_a else None,
        "identity_b": identity_b.redacted(),
        "marker_a_supplied": bool(args.victim_marker),
        "scope": scope_patterns,
        "lead_only": True,
    }
    out_dir = args.out
    if not out_dir:
        host = scope_patterns[0].replace("*", "wildcard").replace("/", "_").replace(":", "-")
        out_dir = os.path.join("findings", host, "authz")
    results_file = _write_results(out_dir, cases, meta)
    lead_urls = [c.url for c in cases if c.verdict in {
        "CROSS_USER_MARKER", "IDENTICAL_ACROSS_IDENTITIES",
        "SAME_SCHEMA_DIFFERENT_DATA"}]
    if args.recon_dir and lead_urls:
        lead_dir = Path(args.recon_dir) / "authz"
        lead_dir.mkdir(parents=True, exist_ok=True)
        (lead_dir / "leads.txt").write_text("\n".join(lead_urls) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for case in cases:
        counts[case.verdict] = counts.get(case.verdict, 0) + 1
    if not args.json:
        print("\n=== authz differential summary ===")
        for verdict, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {verdict:32s} {count}")
        leads = sum(counts.get(v, 0) for v in
                    ("CROSS_USER_MARKER", "IDENTICAL_ACROSS_IDENTITIES", "SAME_SCHEMA_DIFFERENT_DATA"))
        print(f"  leads: {leads} | results: {results_file}")
        if leads:
            print("  LEAD-only: verify with /validate (two identities + marker) before reporting.")
    return 0


def main(argv: list[str] | None = None) -> int:
    return _main(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    raise SystemExit(main())
