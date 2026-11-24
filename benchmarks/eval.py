#!/usr/bin/env python3
"""Reproducible benchmark harness: run identical suites against a repo checkout."""
import argparse, json, os, subprocess, sys, time

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "web3")
EXPECT = {"seen_bad.sol": "detect", "unseen_bad.sol": "detect",
          "seen_good.sol": "clean", "unseen_good.sol": "clean"}


def sh(cmd, cwd, timeout=600):
    t = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr, round(time.time() - t, 2)


def run(repo, label):
    res = {"label": label, "repo": repo, "stages": {}}
    py = sys.executable
    # 1) unit suite
    rc, out, err, dt = sh([py, "-m", "pytest", "-q"], repo)
    tail = [l for l in (out or "").splitlines() if "passed" in l or "failed" in l]
    res["stages"]["pytest"] = {"rc": rc, "summary": tail[-1] if tail else "", "sec": dt}

    # 2) verifier benchmark
    rc, out, err, dt = sh([py, "tests/benchmark/score.py", "--json"], repo)
    try:
        d = json.loads(out); res["stages"]["verifier_bench"] = {
            "counts": d.get("counts"), "precision": d.get("precision"),
            "recall": d.get("recall"), "fp_rate": d.get("fp_rate"), "sec": dt}
    except Exception:
        res["stages"]["verifier_bench"] = {"rc": rc, "error": "no json", "sec": dt}

    # 3) authz benchmark
    rc, out, err, dt = sh([py, "tests/benchmark/authz_score.py", "--json"], repo)
    try:
        d = json.loads(out); res["stages"]["authz_bench"] = {
            "recall": d.get("recall"), "confirmed_fp": d.get("confirmed_fp"),
            "verdict_accuracy": d.get("verdict_accuracy"), "sec": dt}
    except Exception:
        res["stages"]["authz_bench"] = {"rc": rc, "error": "no json", "sec": dt}

    # 4) web3 access-control detection on fixed fixtures (seen + UNSEEN)
    scanner = os.path.join(repo, "bughunter", "tools", "web3_evm_hazard_scan.py")
    w3 = {}
    for f, want in EXPECT.items():
        path = os.path.join(FIX, f)
        rc, out, err, dt = sh([py, scanner, "--json", path], repo)
        try:
            rules = [x.get("rule") for x in json.loads(out)]
        except Exception:
            rules = []
        hit = rules.count("ACCESS-CONTROL-01")
        ok = (hit > 0) if want == "detect" else (hit == 0)
        w3[f] = {"expected": want, "detections": hit, "pass": ok}
    res["stages"]["web3_access_control"] = {
        "fixtures": w3, "passed": sum(v["pass"] for v in w3.values()), "total": len(w3)}

    res["verdict"] = _verdict(res)
    return res


def _verdict(r):
    st = r["stages"]
    s = 0
    if st["pytest"]["rc"] == 0: s += 1
    if (st.get("verifier_bench") or {}).get("recall") == 1.0 and (st["verifier_bench"].get("counts", {}).get("FP") == 0): s += 1
    if (st.get("authz_bench") or {}).get("recall") == 1.0 and st["authz_bench"].get("confirmed_fp") == 0: s += 1
    if st["web3_access_control"]["passed"] == st["web3_access_control"]["total"]: s += 1
    return f"{s}/4 gates"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    r = run(os.path.abspath(a.repo), a.label)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(r, open(a.out, "w"), indent=2)
    print(json.dumps(r, indent=2))


if __name__ == "__main__":
    main()
