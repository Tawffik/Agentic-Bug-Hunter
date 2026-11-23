#!/usr/bin/env python3
"""Authorized end-to-end bug-bounty target — a small app with LOGIN + a full
set of bug classes, for exercising the whole toolkit 0->final.

Not a benchmark of one gate: this is the target the "full flow" runner drives
end-to-end (recon -> login -> hunt -> authz -> validate -> report -> outcome).

Bugs (ground truth):
  1. open-redirect   /go?url=            (302 honors any Location)
  2. sensitive-file  /.env               (leaks FLAG + AWS-style secret)
  3. sqli            /search?q=          (error-based + time-based SLEEP)
  4. bola-orders     /api/orders/{id}    (any user reads any order)
  5. bola-users      /api/users/{id}     (any user reads any profile)
  6. auth-bypass     /admin              (anon 200 with Admin Panel + FLAG)

Auth: POST /login {username,password} -> Set-Cookie sess=<user>.
Users: alice/password1 (owner of order 1), bob/password2 (owner of order 2).

Binds 127.0.0.1 only. DO NOT DEPLOY.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("FULL_HOST", "127.0.0.1")
PORT = int(os.environ.get("FULL_PORT", "8098"))
FLAG = os.environ.get("FULL_FLAG") or f"FLAG{{{secrets.token_hex(8)}}}"

USERS = {"alice": "password1", "bob": "password2"}
EMAIL = {"alice": "alice@example.test", "bob": "bob@example.test"}
ORDERS = {"1": ("alice", 4242), "2": ("bob", 777)}
PROFILES = {"1": ("alice@example.test", "Alice"), "2": ("bob@example.test", "Bob")}

_SLEEP_RE = re.compile(r"sleep\(\s*(\d+)\s*\)", re.I)

APP_JS = ("const API = {\n"
          "  me: '/api/me',\n"
          "  order: (id) => `/api/orders/${id}`,\n"
          "  orders: ['/api/orders/1', '/api/orders/2'],\n"
          "  users: ['/api/users/1', '/api/users/2'],\n"
          "  stats: '/api/admin/stats',\n"
          "};\n")

LANDING = ("<html><body><h1>Acme Portal</h1>"
           "<a href='/login'>Login</a> "
           "<a href='/docs'>API docs</a> "
           "<a href='/app'>App</a></body></html>")

DOCS = ("<html><body><h1>API</h1>"
        "<p>GET /api/me</p><p>GET /api/orders/1</p><p>GET /api/orders/2</p>"
        "<p>GET /api/users/1</p><p>GET /api/users/2</p></body></html>")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # noqa: A003
        pass

    def _who(self):
        c = self.headers.get("Cookie", "")
        for u in USERS:
            if f"sess={u}" in c:
                return u
        return "anon"

    def _send(self, status, body, ctype="text/plain; charset=utf-8", extra=None):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status, payload, extra=None):
        self._send(status, json.dumps(payload), "application/json", extra)

    def do_GET(self):  # noqa: N802
        p = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(p.query, keep_blank_values=True)
        who = self._who()
        path = p.path

        if path == "/":
            return self._send(200, LANDING, "text/html")
        if path == "/docs":
            return self._send(200, DOCS, "text/html")
        if path == "/robots.txt":
            return self._send(200, "User-agent: *\nDisallow: /admin\n"
                                   "Disallow: /.env\nAllow: /api\n")
        if path == "/app.js":
            return self._send(200, APP_JS, "application/javascript")
        if path == "/login":
            return self._send(200, "<form method=post action=/login>"
                                   "<input name=username><input name=password "
                                   "type=password><button>Login</button></form>",
                              "text/html")
        if path == "/app":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            return self._send(200, "<html><body><div id=root>App</div>"
                                   "<script src='/app.js'></script></body></html>",
                              "text/html")
        if path == "/.env":
            return self._send(200, "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n"
                                   "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/"
                                   "bPxRfiCYEXAMPLEKEY\nJWT_SIGNING_KEY="
                                   + secrets.token_hex(16) + f"\nFLAG={FLAG}\n")
        if path == "/admin":                      # auth-bypass: anon 200 + marker
            return self._send(200, f"<h1>Admin Panel</h1> owner token: {FLAG}",
                              "text/html")
        if path == "/search":
            payload = q.get("q", [""])[0]
            if "'" in payload:
                return self._send(200, "SQL syntax error near '' at line 1")
            m = _SLEEP_RE.search(payload)
            if m:
                time.sleep(min(int(m.group(1)), 5))
            return self._send(200, "<h2>0 results</h2>")
        if path == "/go":
            return self._send(302, "", extra={"Location": q.get("url", ["/"])[0]})
        if path == "/api/me":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            return self._json(200, {"id": who, "email": EMAIL[who], "name": who.title()})
        if path.startswith("/api/orders/"):
            if who == "anon":
                return self._json(401, {"error": "auth"})
            oid = path.rsplit("/", 1)[-1]
            owner, total = ORDERS.get(oid, ("?", 0))
            return self._json(200, {"id": oid, "owner_email": EMAIL.get(owner, ""),
                                    "owner": owner, "total": total})
        if path.startswith("/api/users/"):
            if who == "anon":
                return self._json(401, {"error": "auth"})
            uid = path.rsplit("/", 1)[-1]
            email, name = PROFILES.get(uid, ("", ""))
            return self._json(200, {"id": uid, "email": email, "name": name})
        if path == "/api/admin/stats":
            if who == "anon":
                return self._json(401, {"error": "auth"})
            return self._json(200, {"users": len(USERS), "orders": len(ORDERS)})
        return self._json(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        if urllib.parse.urlparse(self.path).path == "/login":
            n = int(self.headers.get("Content-Length", 0) or 0)
            form = urllib.parse.parse_qs(self.rfile.read(n).decode("utf-8", "replace"))
            u = (form.get("username") or [""])[0]
            pw = (form.get("password") or [""])[0]
            if USERS.get(u) == pw and pw:
                return self._json(200, {"ok": True, "user": u},
                                  extra={"Set-Cookie": f"sess={u}; Path=/"})
            return self._json(401, {"error": "invalid credentials"})
        return self._json(404, {"error": "not found"})


def main() -> int:
    print(f"[full] target on http://{HOST}:{PORT}  flag={FLAG}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
