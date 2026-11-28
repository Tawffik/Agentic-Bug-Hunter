#!/usr/bin/env python3
"""Harness-held capture seal for verifier traces (opt-in, off by default).

Why: an agent can write any evidence text and compute any sha256. It cannot compute an
HMAC under a key it never sees. When a sealer is active, every HttpExchange that
`base.fetch` records is stamped with sha256 + seal, so a downstream gate can tell
"the harness's own fetch recorded these bytes" from "the agent claimed them".

Algorithm matches security-research-agent `agent_core.harness.seal.Sealer`:
    seal = HMAC-SHA256(key, "\\x1f".join([kind, ref, role, sha256]))
Key handling: pass a key via `ZT_SEAL_KEY_FILE` (path to a file holding hex) or let the
process generate a random one. The key is never logged or written by this module.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets

KIND = "http"


def exchange_text(method: str, url: str, status, snippet: str) -> str:
    """Canonical text of an exchange that gets hashed and sealed."""
    return f"{method} {url}\nstatus={status}\n{snippet}"


class CaptureSealer:
    def __init__(self, key: bytes | None = None):
        self._key = key or secrets.token_bytes(32)

    @classmethod
    def from_env(cls) -> "CaptureSealer":
        path = os.environ.get("ZT_SEAL_KEY_FILE", "")
        if path and os.path.isfile(path):
            with open(path) as fh:
                return cls(bytes.fromhex(fh.read().strip()))
        return cls()

    def _mac(self, kind: str, ref: str, role: str, sha: str) -> str:
        msg = "\x1f".join([kind, ref, role, sha]).encode()
        return hmac.new(self._key, msg, hashlib.sha256).hexdigest()

    def stamp(self, ex, role: str = "") -> None:
        """Fill ex.content, ex.sha256, ex.seal, ex.role in place."""
        raw = exchange_text(ex.method, ex.url, ex.status, ex.response_snippet)
        ex.content = raw
        ex.sha256 = hashlib.sha256(raw.encode()).hexdigest()
        ex.role = role
        ex.seal = self._mac(KIND, ex.url, role, ex.sha256)

    def valid(self, ex) -> bool:
        if not ex.seal or not ex.sha256:
            return False
        if hashlib.sha256(ex.content.encode()).hexdigest() != ex.sha256:
            return False
        return hmac.compare_digest(ex.seal, self._mac(KIND, ex.url, ex.role, ex.sha256))
