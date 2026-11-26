"""Engagement contract — one declarative, fail-closed file per engagement.

Adopted from the AgntX-Hunter scope.json pattern (MIT, reviewed 2026-11-26)
and grounded against ARTEX's in-scope DSL checks. This module is the single
place that binds: authorization status, scope patterns, rules of engagement
(no_dos / no_destructive / RPS), and tool-execution consent. The deterministic
URL check itself stays in tools/scope_checker.py (hardened, fail-closed);
this file only feeds it.

Fail-closed rules:
  - missing/unparseable file           -> EngagementError at load
  - status != "authorized"             -> require_authorized() raises
  - empty in_scope                     -> EngagementError at load
  - unknown keys are rejected          -> no silent config drift
"""
from __future__ import annotations

import json
import threading
import time

from .scope_checker import ScopeChecker

_VALID_STATUS = {"pending_authorization", "authorized", "expired", "revoked"}
_KNOWN_KEYS = {
    "name", "status", "in_scope", "out_of_scope", "excluded_classes",
    "no_destructive", "no_dos", "requests_per_second",
    "allow_external_recon_tools", "approval_required", "notes",
}


class EngagementError(ValueError):
    """Unusable or unauthorized engagement configuration."""


class Engagement:
    def __init__(self, data: dict):
        if not isinstance(data, dict):
            raise EngagementError("engagement file must contain a JSON object")
        unknown = set(data) - _KNOWN_KEYS
        if unknown:
            raise EngagementError(f"unknown engagement keys: {sorted(unknown)}")
        self.name = str(data.get("name") or "unnamed")
        self.status = str(data.get("status") or "pending_authorization")
        if self.status not in _VALID_STATUS:
            raise EngagementError(f"unknown status: {self.status!r}")
        self.in_scope = list(data.get("in_scope") or [])
        self.out_of_scope = list(data.get("out_of_scope") or [])
        self.excluded_classes = list(data.get("excluded_classes") or [])
        if not self.in_scope:
            raise EngagementError("in_scope must not be empty (fail-closed)")
        self.no_destructive = bool(data.get("no_destructive", True))
        self.no_dos = bool(data.get("no_dos", True))
        rps = data.get("requests_per_second", 2)
        self.requests_per_second = float(rps) if rps else 0.0
        if self.requests_per_second < 0:
            raise EngagementError("requests_per_second must be >= 0")
        self.allow_external_recon_tools = bool(data.get("allow_external_recon_tools", False))
        self.approval_required = bool(data.get("approval_required", False))
        self.notes = str(data.get("notes") or "")

    @classmethod
    def load(cls, path: str) -> "Engagement":
        try:
            with open(path, encoding="utf-8") as fh:
                return cls(json.load(fh))
        except FileNotFoundError as exc:
            raise EngagementError(f"engagement file not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise EngagementError(f"engagement file is not valid JSON: {exc}") from exc

    def require_authorized(self) -> None:
        """Hard gate: call before any outbound work."""
        if self.status != "authorized":
            raise EngagementError(
                f"engagement {self.name!r} is {self.status}, not authorized — "
                "written authorization required before any request"
            )

    def scope_checker(self) -> ScopeChecker:
        return ScopeChecker(
            domains=self.in_scope,
            excluded_domains=self.out_of_scope,
            excluded_classes=self.excluded_classes + (["dos"] if self.no_dos else []),
        )

    def rate_limiter(self) -> "TokenBucket":
        rps = self.requests_per_second or 2.0
        return TokenBucket(rate_per_second=rps)


class TokenBucket:
    """Minimal per-process token bucket (thread-safe)."""

    def __init__(self, rate_per_second: float):
        self._interval = 1.0 / max(rate_per_second, 0.01)
        self._lock = threading.Lock()
        self._next_ok = 0.0

    def acquire(self) -> float:
        """Block until a token is available; returns the wait in seconds."""
        with self._lock:
            now = time.monotonic()
            wait = max(0.0, self._next_ok - now)
            self._next_ok = max(now, self._next_ok) + self._interval
        if wait:
            time.sleep(wait)
        return wait


TEMPLATE = {
    "name": "example-engagement",
    "status": "pending_authorization",
    "in_scope": ["*.example.com", "example.com"],
    "out_of_scope": ["admin.example.com"],
    "no_destructive": True,
    "no_dos": True,
    "requests_per_second": 2,
    "allow_external_recon_tools": False,
    "approval_required": False,
    "notes": "Replace with written authorization before use.",
}


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys
    ap = argparse.ArgumentParser(description="Engagement contract check")
    ap.add_argument("engagement", help="path to engagement JSON")
    ap.add_argument("--check-url", help="validate one URL against the engagement scope")
    ap.add_argument("--init", action="store_true", help="write a template to the given path")
    args = ap.parse_args(argv)
    if args.init:
        with open(args.engagement, "w", encoding="utf-8") as fh:
            json.dump(TEMPLATE, fh, indent=2)
        print(f"template written: {args.engagement} (status stays pending_authorization)")
        return 0
    try:
        eng = Engagement.load(args.engagement)
    except EngagementError as exc:
        print(f"ENGAGEMENT ERROR: {exc}", file=sys.stderr)
        return 2
    if args.check_url:
        try:
            eng.require_authorized()
        except EngagementError as exc:
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 3
        ok = eng.scope_checker().is_in_scope(args.check_url)
        print(("IN SCOPE: " if ok else "OUT OF SCOPE: ") + args.check_url)
        return 0 if ok else 4
    print(f"engagement {eng.name!r}: status={eng.status} rps={eng.requests_per_second} "
          f"no_dos={eng.no_dos} no_destructive={eng.no_destructive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
