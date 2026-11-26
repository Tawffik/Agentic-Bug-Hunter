"""Traffic capture + execution visibility for tool runs.

Two pieces, both grounded in ARTEX source reviewed 2026-11-26:

1. proxy_env() — the env matrix that routes a subprocess's HTTP through a
   recording proxy (agent/worker.go proxyEnv): HTTP(S)_PROXY + ALL_PROXY for
   socks egress, NODE_USE_ENV_PROXY for Node 24+, and the per-ecosystem CA
   variables so TLS tooling trusts the recording MITM without per-tool flags.
   Empty proxy address -> empty dict (caller's env stays untouched).

2. capture_run() — the capture.go pattern: run one tool and append structured
   activity records (tool_use / tool_result) to a JSONL audit log, so every
   hunt keeps a reviewable execution trail instead of a black box.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime, timezone


def proxy_env(proxy_addr: str, ca_cert: str = "") -> dict[str, str]:
    """Env vars routing child-process HTTP(S) through proxy_addr."""
    if not proxy_addr:
        return {}
    env = {
        "HTTP_PROXY": proxy_addr, "HTTPS_PROXY": proxy_addr,
        "http_proxy": proxy_addr, "https_proxy": proxy_addr,
        # socks5 egress: curl only reads ALL_PROXY for socks
        "ALL_PROXY": proxy_addr, "all_proxy": proxy_addr,
        # Node 24+: honor HTTP(S)_PROXY in built-in fetch/http
        "NODE_USE_ENV_PROXY": "1",
    }
    if ca_cert:
        env.update({
            "SSL_CERT_FILE": ca_cert,        # curl/urllib/Go/openssl
            "REQUESTS_CA_BUNDLE": ca_cert,   # python requests ignores SSL_CERT_FILE
            "CURL_CA_BUNDLE": ca_cert,       # curl explicit
            "GIT_SSL_CAINFO": ca_cert,       # git
            "NODE_EXTRA_CA_CERTS": ca_cert,  # node
        })
    return env


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def capture_run(cmd: list[str], log_path: str, *, proxy_addr: str = "",
                ca_cert: str = "", timeout: int = 300, tail: int = 400) -> int:
    """Run cmd with the proxy env matrix, appending activity records to log_path.

    Records carry kind/ts/cmd/exit/duration_ms and bounded stdout/stderr tails
    (never unbounded capture). Returns the child exit code.
    """
    env = dict(os.environ)
    env.update(proxy_env(proxy_addr, ca_cert))
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)

    def _emit(rec: dict) -> None:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    _emit({"kind": "tool_use", "ts": _now(), "cmd": cmd,
           "proxied": bool(proxy_addr)})
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True,
                              timeout=timeout, errors="replace")
        code, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        code, out, err = 124, "", f"timeout after {timeout}s"
    dur = int((time.monotonic() - start) * 1000)
    _emit({"kind": "tool_result", "ts": _now(), "cmd": cmd, "exit": code,
           "duration_ms": dur, "stdout_tail": out[-tail:], "stderr_tail": err[-tail:]})
    return code


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Run a tool under traffic capture")
    ap.add_argument("--log", required=True, help="activity JSONL path")
    ap.add_argument("--proxy", default="", help="recording proxy addr, e.g. http://127.0.0.1:8080")
    ap.add_argument("--ca", default="", help="MITM CA cert path")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)
    if not args.cmd:
        ap.error("no command given")
    return capture_run(args.cmd, args.log, proxy_addr=args.proxy, ca_cert=args.ca)


if __name__ == "__main__":
    raise SystemExit(main())
