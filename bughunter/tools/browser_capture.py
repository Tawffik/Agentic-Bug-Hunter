#!/usr/bin/env python3
"""Authenticated browser capture for SPA / JS-heavy targets.

Opens a URL in Chromium, optionally with a saved Playwright storage state,
cookies, or extra headers, then captures:
  - final URL, title, screenshot
  - network requests/responses (method, URL, status, content-type)
  - localStorage / sessionStorage keys
  - cookie names/domains (values redacted by default)
  - an optional HAR file and a replayable storage-state file

This is deliberately read-only: it loads the page, does not submit forms, and
does not sign transactions. Use it to map authenticated API calls before
sending them to Burp/Caido or the existing IDOR/auth tools.

Examples:
  python3 bughunter/tools/browser_capture.py https://app.example.com
  python3 bughunter/tools/browser_capture.py https://app.example.com \
      --storage-state auth.json --out captures/app
  python3 bughunter/tools/browser_capture.py https://app.example.com \
      --cookie "session=abc" --header "X-Tenant: 42" --headed
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlparse

SECRET_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key", "x-auth-token"}


@dataclass
class RequestRecord:
    method: str
    url: str
    resource_type: str
    status: int | None = None
    content_type: str = ""
    # API-capture (XHR/fetch) fields; populated when --capture-api is set.
    post_data: str = ""
    api_headers: dict = field(default_factory=dict)


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {
        name: ("<redacted>" if name.lower() in SECRET_HEADERS else value)
        for name, value in headers.items()
    }


def parse_cookie_string(raw: str) -> list[dict[str, str]]:
    cookies = []
    for part in raw.split(";"):
        if "=" not in part:
            continue
        name, value = part.split("=", 1)
        name = name.strip()
        if name:
            cookies.append({"name": name, "value": value.strip()})
    return cookies


def parse_headers(values: list[str]) -> dict[str, str]:
    headers = {}
    for raw in values:
        if ":" not in raw:
            raise ValueError(f"invalid header (expected 'Name: value'): {raw[:40]}")
        name, value = raw.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def storage_summary(page) -> dict[str, list[str]]:
    try:
        local = page.evaluate("Object.keys(window.localStorage || {})")
        session = page.evaluate("Object.keys(window.sessionStorage || {})")
    except Exception:
        local, session = [], []
    return {"localStorage": local, "sessionStorage": session}


def run(args) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "playwright is not installed. Install with:\n"
            "  python3 -m pip install --user playwright\n"
            "  python3 -m playwright install chromium"
        ) from exc

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    requests: list[RequestRecord] = []
    blocked_hosts: set[str] = set()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context_args: dict = {"ignore_https_errors": args.ignore_https_errors}
        if args.storage_state:
            context_args["storage_state"] = args.storage_state
        if args.har:
            context_args["record_har_path"] = str(out / "network.har")
        context = browser.new_context(**context_args)

        def route_handler(route):
            request = route.request
            host = urlparse(request.url).netloc.lower()
            if args.allow_host and host not in args.allow_host and request.resource_type in {"xhr", "fetch"}:
                blocked_hosts.add(host)
                route.abort()
                return
            route.continue_()

        if args.allow_host:
            context.route("**/*", route_handler)

        headers = parse_headers(args.header)
        if headers:
            context.set_extra_http_headers(headers)

        cookies = parse_cookie_string(args.cookie) if args.cookie else []
        if cookies:
            base = f"{urlparse(args.url).scheme}://{urlparse(args.url).netloc}"
            for cookie in cookies:
                cookie["url"] = base
            context.add_cookies(cookies)

        page = context.new_page()

        def on_request(request):
            rec = RequestRecord(request.method, request.url, request.resource_type)
            if args.capture_api and request.resource_type in {"xhr", "fetch"}:
                try:
                    pd = request.post_data
                    if pd:
                        rec.post_data = pd[:800]
                except Exception:  # noqa: BLE001
                    pass
                try:
                    rec.api_headers = {
                        k: v for k, v in request.headers.items()
                        if k.lower() not in SECRET_HEADERS
                    }
                except Exception:  # noqa: BLE001
                    pass
            requests.append(rec)

        def on_response(response):
            for record in reversed(requests):
                if record.url == response.url and record.status is None:
                    record.status = response.status
                    record.content_type = response.headers.get("content-type", "")
                    break

        page.on("request", on_request)
        page.on("response", on_response)
        page.goto(args.url, wait_until=args.wait_until, timeout=args.timeout * 1000)
        if args.wait:
            page.wait_for_timeout(args.wait)

        title = page.title()
        final_url = page.url
        if args.screenshot:
            page.screenshot(path=str(out / args.screenshot), full_page=args.full_page)

        summary = storage_summary(page)
        cookie_names = [
            {"name": c.get("name"), "domain": c.get("domain"), "path": c.get("path")}
            for c in context.cookies()
        ]
        if args.storage_state_out:
            context.storage_state(path=args.storage_state_out)

        browser.close()

    report = {
        "url": args.url,
        "final_url": final_url,
        "title": title,
        "screenshot": str(out / args.screenshot) if args.screenshot else "",
        "har": str(out / "network.har") if args.har else "",
        "storage_state_out": args.storage_state_out or "",
        "storage": summary,
        "cookies": cookie_names,
        "blocked_hosts": sorted(blocked_hosts),
        "requests": [asdict(r) for r in requests],
    }
    (out / "capture.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Authenticated Playwright capture for SPA targets.")
    parser.add_argument("url", help="Target URL (http/https)")
    parser.add_argument("--storage-state", help="Playwright storage-state JSON for an authenticated session")
    parser.add_argument("--storage-state-out", help="Write the post-load storage state (contains secrets)")
    parser.add_argument("--cookie", default="", help="Cookie header string: 'a=1; b=2'")
    parser.add_argument("--header", action="append", default=[], help="Extra header (repeatable)")
    parser.add_argument("--out", default="browser-capture", help="Output directory")
    parser.add_argument("--screenshot", default="page.png", help="Screenshot file name")
    parser.add_argument("--full-page", action="store_true", help="Full-page screenshot")
    parser.add_argument("--har", action="store_true", help="Write network.har")
    parser.add_argument("--capture-api", action="store_true",
                        help="Record XHR/fetch request bodies + non-secret headers (e.g. anti-content)")
    parser.add_argument("--wait", type=int, default=1500, help="Extra wait after load (ms)")
    parser.add_argument("--timeout", type=int, default=30, help="Navigation timeout (seconds)")
    parser.add_argument("--wait-until", default="networkidle", choices=["load", "domcontentloaded", "networkidle"])
    parser.add_argument("--headed", action="store_true", help="Show the browser")
    parser.add_argument("--ignore-https-errors", action="store_true", help="Accept invalid TLS certs")
    parser.add_argument("--allow-host", action="append", default=[], help="Only allow XHR/fetch to these hosts")
    parser.add_argument("--json", action="store_true", help="Print the JSON report")
    args = parser.parse_args()

    if args.allow_host:
        args.allow_host = {h.lower() for h in args.allow_host}
    report = run(args)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"url:        {report['url']}")
        print(f"final:      {report['final_url']}")
        print(f"title:      {report['title']}")
        print(f"requests:   {len(report['requests'])}")
        print(f"storage:    localStorage={len(report['storage']['localStorage'])} "
              f"sessionStorage={len(report['storage']['sessionStorage'])}")
        print(f"cookies:    {len(report['cookies'])}")
        print(f"capture:    {Path(args.out) / 'capture.json'}")
        if report["blocked_hosts"]:
            print(f"blocked:    {', '.join(report['blocked_hosts'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
