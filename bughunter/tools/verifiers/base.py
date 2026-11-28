#!/usr/bin/env python3
"""Shared primitives for the deterministic verifier library.

The verifier library is the false-positive killer: a candidate finding is only
a *lead* until an independent, **non-AI** verifier reproduces it against the
live target and a deterministic oracle fires. Verifiers never emit a confidence
score — they return a boolean plus a reproducible request/response trace.

This mirrors XBOW's discovery/validation split: the agent that surfaces a bug is
never the system that confirms it. Everything here is pure plumbing + an
SSRF-safe single-hop fetch; the per-class oracles live in the sibling modules.
"""
from __future__ import annotations

import ssl
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Prefer certifi's CA bundle when available; never disable verification.
_SSL_CTX = ssl.create_default_context()
try:  # pragma: no cover - depends on local install
    import certifi

    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()

USER_AGENT = "agentic-bug-hunter/verifier"

class HostPacer:
    """Per-host minimum spacing between requests (rate_per_min per host). Opt-in via set_pacer()
    or env ZT_RATE_PER_MIN. clock/sleep are injectable so tests never really sleep.
    Best effort: it paces calls that go through fetch(), nothing else."""

    def __init__(self, rate_per_min: float, clock=time.monotonic, sleep=time.sleep):
        self.gap = 60.0 / rate_per_min if rate_per_min and rate_per_min > 0 else 0.0
        self._clock, self._sleep, self._next = clock, sleep, {}
        self.waited = 0.0

    def wait(self, host: str) -> float:
        if not self.gap:
            return 0.0
        now = self._clock()
        due = self._next.get(host, now)
        delay = max(0.0, due - now)
        if delay:
            self._sleep(delay)
            self.waited += delay
        self._next[host] = max(now, due) + self.gap
        return delay


_PACER = None


def set_pacer(pacer) -> None:
    """Activate (or with None, deactivate) per-host pacing for `fetch`."""
    global _PACER
    _PACER = pacer


def _pace(url: str) -> None:
    global _PACER
    if _PACER is None:
        import os
        try:
            rate = float(os.environ.get("ZT_RATE_PER_MIN", "") or 0)
        except ValueError:
            rate = 0
        if rate > 0:
            _PACER = HostPacer(rate)
    if _PACER is not None:
        _PACER.wait((urlparse(url).hostname or "").lower())


_SEALER = None  # opt-in: set_sealer(CaptureSealer.from_env()) stamps every fetched exchange


def set_sealer(sealer) -> None:
    """Activate (or with None, deactivate) capture sealing for `fetch`."""
    global _SEALER
    _SEALER = sealer


def _stamp(ex: "HttpExchange", role: str) -> "HttpExchange":
    if _SEALER is not None:
        _SEALER.stamp(ex, role)
    return ex


@dataclass
class HttpExchange:
    """One request/response pair in a verifier's reproducible trace."""

    method: str
    url: str
    status: int | None
    request_headers: dict
    response_headers: dict
    response_snippet: str
    elapsed_ms: float
    note: str = ""
    # Filled only when a CaptureSealer is active (see verifiers/seal.py). Empty otherwise.
    content: str = ""
    sha256: str = ""
    role: str = ""
    seal: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class VerifyResult:
    """The verdict of a verifier run.

    confirmed=True means a deterministic oracle fired — the bug is real and
    reproducible via `trace`. skipped=True means the verifier could not run
    (missing dependency, missing creds, no OOB callback); it is NOT a pass and
    NOT a fail — the finding stays an unverified lead.
    """

    confirmed: bool
    vuln_class: str
    oracle: str
    trace: list[HttpExchange] = field(default_factory=list)
    evidence: str = ""
    error: str | None = None
    skipped: bool = False

    def to_dict(self) -> dict:
        return {
            "confirmed": self.confirmed,
            "vuln_class": self.vuln_class,
            "oracle": self.oracle,
            "evidence": self.evidence,
            "error": self.error,
            "skipped": self.skipped,
            "trace": [x.to_dict() for x in self.trace],
        }


def confirmed(vuln_class: str, oracle: str, trace: list[HttpExchange], evidence: str) -> VerifyResult:
    return VerifyResult(True, vuln_class, oracle, trace, evidence)


def rejected(vuln_class: str, oracle: str, trace: list[HttpExchange], evidence: str = "") -> VerifyResult:
    return VerifyResult(False, vuln_class, oracle, trace, evidence or "oracle did not fire")


def skipped(vuln_class: str, reason: str) -> VerifyResult:
    return VerifyResult(False, vuln_class, reason, [], "", error=reason, skipped=True)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never auto-follow; verifiers inspect raw 3xx + Location themselves."""

    def redirect_request(self, *args, **kwargs):  # noqa: D401
        return None


def _opener(context: ssl.SSLContext | None):
    handlers: list = [_NoRedirect]
    if context is not None:
        handlers.append(urllib.request.HTTPSHandler(context=context))
    return urllib.request.build_opener(*handlers)


def fetch(
    url: str,
    *,
    method: str = "GET",
    headers: dict | None = None,
    data: bytes | None = None,
    timeout: float = 15.0,
    scope_checker=None,
    note: str = "",
    max_body: int = 65536,
    role: str = "",
) -> tuple[HttpExchange, bytes]:
    """Single-hop fetch (no redirect following) returning a trace entry + body.

    Redirects are never followed, so a target cannot 302 us into cloud metadata
    or an RFC1918 host — the SSRF seam `safe_http` guards. When a scope_checker
    is supplied, an out-of-scope URL is refused before any socket is opened.
    """
    headers = dict(headers or {})
    headers.setdefault("User-Agent", USER_AGENT)

    if scope_checker is not None and not scope_checker.is_in_scope(url):
        ex = HttpExchange(method, url, None, headers, {}, "", 0.0,
                          note or "blocked: out of scope")
        return _stamp(ex, role), b""

    _pace(url)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = _opener(_SSL_CTX)
    start = time.perf_counter()
    status: int | None
    resp_headers: dict = {}
    body = b""
    try:
        resp = opener.open(req, timeout=timeout)
        status = getattr(resp, "status", None) or resp.getcode()
        resp_headers = dict(resp.headers.items())
        body = resp.read(max_body)
    except urllib.error.HTTPError as exc:
        # HTTPError doubles as a response object (incl. 3xx when not followed).
        status = exc.code
        try:
            resp_headers = dict(exc.headers.items())
        except Exception:  # noqa: BLE001
            resp_headers = {}
        try:
            body = exc.read(max_body)
        except Exception:  # noqa: BLE001
            body = b""
    except Exception as exc:  # noqa: BLE001 - a dead host shouldn't crash the sweep
        elapsed = (time.perf_counter() - start) * 1000
        ex = HttpExchange(method, url, None, headers, {}, "", elapsed,
                          note or f"{type(exc).__name__}: {exc}")
        return _stamp(ex, role), b""

    elapsed = (time.perf_counter() - start) * 1000
    snippet = body[:2048].decode("utf-8", "replace")
    ex = HttpExchange(method, url, status, headers, resp_headers, snippet, elapsed, note)
    return _stamp(ex, role), body


def set_param(url: str, param: str, value: str) -> str:
    """Return `url` with query `param` set to `value` (preserving the rest)."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query, keep_blank_values=True)
    query[param] = [value]
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def finding_url(finding: dict) -> str:
    """Pull the testable URL out of a finding dict (url or endpoint)."""
    return str(finding.get("url") or finding.get("endpoint") or "").strip()
