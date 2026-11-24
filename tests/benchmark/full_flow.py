#!/usr/bin/env python3
"""Full bug-bounty lifecycle runner — 0 to final, on ONE authorized target.

Stages: scope -> boot -> login (two identities) -> recon/discovery ->
JS mining -> lead ingest -> hidden-param discovery -> unauth verifier swarm ->
two-identity authz differential (+ deterministic IDOR confirm) -> outcome ->
report draft -> scorecard vs ground truth.

Usage:
  python3 tests/benchmark/full_flow.py --json

Kept in the repo as the end-to-end regression for the whole pipeline (not just
one gate). Binds/attacks 127.0.0.1 only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request
from http.client import HTTPConnection

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for _p in (_REPO, os.path.join(_REPO, "bughunter")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tools import lead_board, swarm, param_probe  # noqa: E402
from tools.hunt_outcome import analyze  # noqa: E402
from tools.scope_checker import ScopeChecker  # noqa: E402
from tools.authz_diff import Identity, Scanner  # noqa: E402

PORT = 8098
BASE = f"http://127.0.0.1:{PORT}"
TARGET = "bench-full"
RECON = os.path.join(_REPO, "recon", TARGET)
WORDLIST = os.path.join(_REPO, "bughunter", "wordlists", "common.txt")
NESTED = os.path.join(_REPO, "bughunter", "wordlists", "api-nested.txt")

GROUND_TRUTH = {
    "/go": "open-redirect", "/.env": "sensitive-file", "/search": "sqli",
    "/api/orders/1": "bola-orders", "/api/users/1": "bola-users", "/admin": "auth-bypass",
}


def wait_port(host, port, timeout=10.0):
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            s.settimeout(0.4)
            if s.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.1)
    return False


def run(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 1, "", "err"


def http(method, path, body=None, cookie=None):
    c = HTTPConnection("127.0.0.1", PORT, timeout=8)
    hdrs = {"Content-Type": "application/x-www-form-urlencoded"} if body else {}
    if cookie:
        hdrs["Cookie"] = cookie
    c.request(method, path, body=body, headers=hdrs)
    r = c.getresponse()
    data = r.read()
    sc = r.getheader("Set-Cookie")
    c.close()
    return r.status, data.decode("utf-8", "replace"), sc


def login(user, pw):
    st, _, sc = http("POST", "/login", body=f"username={user}&password={pw}")
    if st == 200 and sc:
        return sc.split(";")[0]
    return None


def stage_discovery():
    os.makedirs(os.path.join(RECON, "urls"), exist_ok=True)
    os.makedirs(os.path.join(RECON, "live"), exist_ok=True)
    os.makedirs(os.path.join(RECON, "dirs"), exist_ok=True)
    disc = set()
    log = {}

    st, body, _ = http("GET", "/robots.txt")
    if st == 200:
        for line in body.splitlines():
            m = re.match(r"(?i)disallow:\s*(\S+)", line.strip())
            if m and m.group(1) not in ("", "/"):
                disc.add(m.group(1))
    log["robots"] = st

    rc, out, _ = run(["katana", "-u", BASE, "-d", "2", "-silent", "-nc"], timeout=90)
    for u in (out or "").splitlines():
        p = re.sub(r"^https?://[^/]+", "", u.strip())
        if p and p != "/":
            disc.add(p)
    log["katana"] = len((out or "").splitlines())

    for wl in (WORDLIST, NESTED):
        if not os.path.isfile(wl):
            continue
        rc, out, _ = run(["ffuf", "-u", BASE + "/FUZZ", "-w", wl, "-mc", "all",
                          "-fc", "404", "-s"], timeout=200)
    # ffuf -s prints matched paths on stdout (one per line)
        for line in (out or "").splitlines():
            line = line.strip()
            if line.startswith("/"):
                disc.add(line)
    log["ffuf_done"] = True

    # JS mining: pull endpoints out of the app bundle.
    st, js, _ = http("GET", "/app.js")
    if st == 200:
        for m in re.finditer(r"/api/[a-zA-Z0-9_/]+", js):
            disc.add(m.group(0))
    log["js_endpoints"] = sorted(x for x in disc if x.startswith("/api"))

    urls = sorted({BASE + p for p in disc})
    with open(os.path.join(RECON, "urls", "all.txt"), "w") as f:
        f.write("\n".join(urls) + "\n")
    with open(os.path.join(RECON, "live", "urls.txt"), "w") as f:
        f.write(BASE + "\n")
    return urls, log


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    env = dict(os.environ, FULL_HOST="127.0.0.1", FULL_PORT=str(PORT))
    proc = subprocess.Popen([sys.executable,
                             os.path.join(_REPO, "tests", "benchmark", "full_target.py")],
                            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out = {"target": TARGET, "stages": {}}
    try:
        if not wait_port("127.0.0.1", PORT):
            print("target failed to boot")
            return 1

        # Stage: login (two identities)
        ca, cb = login("alice", "password1"), login("bob", "password2")
        out["stages"]["login"] = {"alice": bool(ca), "bob": bool(cb)}
        assert ca and cb, "login failed"

        # Stage: discovery
        urls, dlog = stage_discovery()
        found = [p for p in GROUND_TRUTH if any(u.endswith(p) or p in u for u in urls)]
        out["stages"]["discovery"] = {
            "endpoints_found": len(urls),
            "ground_truth_found": found,
            "ground_truth_total": len(GROUND_TRUTH), "log": dlog,
        }

        # Stage: hidden params
        sc = ScopeChecker(["127.0.0.1"])
        hits = param_probe.discover([BASE + "/search", BASE + "/go"],
                                    scope_checker=sc, max_urls=5, delay=0.0)
        out["stages"]["params"] = [h["param"] for h in hits]
        wpath = os.path.join(RECON, "urls", "with_params.txt")
        with open(wpath, "w") as f:
            f.write("\n".join(h["probe_url"] for h in hits) + "\n")

        # Stage: lead ingest + swarm (unauthenticated verifiers)
        for p in (f"bughunter/memory/leads/{TARGET}.jsonl",
                  f"bughunter/memory/leads/{TARGET}.jsonl.lock",
                  os.path.join(_REPO, "bughunter", "findings", TARGET)):
            if os.path.isdir(p):
                import shutil; shutil.rmtree(p)
            elif os.path.exists(p):
                os.remove(p)
        leads = lead_board.ingest(TARGET, RECON)
        sw = swarm.coordinate(TARGET, scope_domains=["127.0.0.1"], workers=4)
        out["stages"]["ingest_swarm"] = {
            "leads": len(leads),
            "by_skill": _count(leads, "skill"),
            "swarm": sw.get("summary"),
        }

        # Stage: two-identity authz differential (+ confirm)
        scanner = Scanner(identity_a=Identity("alice", {"Cookie": ca}),
                          identity_b=Identity("bob", {"Cookie": cb}),
                          marker_a="alice@example.test", marker_b="bob@example.test",
                          delay=0.0, scope_checker=sc, confirm=True)
        authz = []
        for u in urls:
            case = scanner.scan(u)
            if case.object_ref:
                authz.append({
                    "url": re.sub(r"^https?://[^/]+", "", u),
                    "verdict": case.verdict,
                    "confirmed": bool(case.verifier and case.verifier.get("technically_confirmed")),
                    "oracle": (case.verifier or {}).get("oracle"),
                })
        out["stages"]["authz"] = authz
        # Record confirmed IDOR leads back to the board so outcome/report see them.
        for a in authz:
            if a["confirmed"]:
                lead_board.add(TARGET, "hunt-idor", BASE + a["url"],
                               "two-identity BOLA confirmed", "high")

        # Stage: outcome
        outcome = analyze(TARGET)
        out["stages"]["outcome"] = {"verdict": outcome["verdict"], "counts": outcome["counts"]}

        # Stage: report (final) — draft a submission for the strongest confirm.
        report_path = _write_report(urls, authz, sw)
        out["stages"]["report"] = report_path

        # Stage: scorecard — did an oracle fire for each ground-truth bug?
        verified = {(r.get("skill")) for r in sw.get("results", []) if r.get("outcome") in ("verified", "needs-chain")}
        oracle_fired = {
            "/go": "hunt-open-redirect" in {r.get("skill") for r in sw.get("results", []) if r.get("outcome") == "needs-chain"},
            "/.env": "hunt-source-leak" in verified,
            "/search": "hunt-sqli" in verified,
            "/api/orders/1": any(a["confirmed"] and a["url"] == "/api/orders/1" for a in authz),
            "/api/users/1": any(a["confirmed"] and a["url"] == "/api/users/1" for a in authz),
            "/admin": False,  # needs an authorized-only marker
        }
        out["scorecard"] = {
            "ground_truth": GROUND_TRUTH,
            "oracle_fired": oracle_fired,
            "confirmed_count": sum(oracle_fired.values()),
            "total": len(GROUND_TRUTH),
        }
        print(json.dumps(out, indent=2, sort_keys=True) if args.json else _pretty(out))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            proc.kill()
    return 0


def _count(rows, key):
    d = {}
    for r in rows:
        d[r.get(key, "?")] = d.get(r.get(key, "?"), 0) + 1
    return d


def _write_report(urls, authz, sw):
    """Draft a submission for the strongest confirmed finding (0->final)."""
    outdir = os.path.join(_REPO, "findings", TARGET)
    os.makedirs(outdir, exist_ok=True)
    conf = [a for a in authz if a["confirmed"]]
    lines = [f"# [BOLA] Cross-tenant object read in {TARGET} API allows any user to read another user's orders/profiles",
             "", "## Summary",
             "An authenticated user can read another user's private objects by requesting them "
             "directly. Confirmed with two identities: identity B (victim) owner of the object, "
             "identity A (attacker) retrieves it, and an anonymous request is denied.", ""]
    if conf:
        lines += ["## Confirmed endpoints (two-identity oracle)", ""]
        for a in conf:
            lines.append(f"- `{a['url']}` — {a['verdict']} — oracle: {a['oracle']}")
        lines += ["", "## Reproduction",
                  "```bash",
                  "# victim owns the object; attacker reads it",
                  f"curl -s -b 'sess=bob' {BASE}{conf[0]['url']}",
                  "```", "",
                  "## Impact",
                  "Cross-tenant read of other users' order/profile data — confidentiality break.", "",
                  "## CVSS 3.1",
                  "AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N = 6.5 (Medium)", ""]
    verified = [r for r in sw.get("results", []) if r.get("outcome") in ("verified", "needs-chain")]
    if verified:
        lines += ["## Additional oracle-confirmed findings", ""]
        for r in verified:
            lines.append(f"- {r.get('skill')}: {r.get('oracle')}")
    path = os.path.join(outdir, "report.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def _pretty(out):
    s = out["stages"]
    lines = [f"FULL FLOW — {out['target']}",
             f"login: alice={s['login']['alice']} bob={s['login']['bob']}",
             f"discovery: {s['discovery']['endpoints_found']} endpoints "
             f"({len(s['discovery']['ground_truth_found'])}/{s['discovery']['ground_truth_total']} ground-truth found)",
             f"params: {s['params']}",
             f"leads/swarm: {s['ingest_swarm']}",
             "authz (two-identity):"]
    for a in s["authz"]:
        lines.append(f"  {a['url']:18} {a['verdict']:22} confirmed={a['confirmed']}")
    lines.append(f"outcome: {s['outcome']}")
    sc = out["scorecard"]
    lines.append(f"SCORECARD: {sc['confirmed_count']}/{sc['total']} bugs oracle-confirmed")
    lines.append("  " + ", ".join(f"{k}={'yes' if v else 'no'}" for k, v in sc["oracle_fired"].items()))
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
