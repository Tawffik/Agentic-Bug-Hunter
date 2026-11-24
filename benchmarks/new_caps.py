#!/usr/bin/env python3
"""New-capability + failure-recovery checks (upgraded-only; N/A for baseline)."""
import json, os, subprocess, sys
REPO = "/workspaces/Agentic-Bug-Hunter"; PY = sys.executable

def sh(cmd, cwd=REPO):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout, p.stderr

out = {"capabilities": {}}
# 1) new-tool unit suites
tests = ["tests/test_api_probe.py", "tests/test_fuzz_diff.py", "tests/test_param_probe.py",
         "tests/test_hunt_outcome.py", "tests/test_skill_registry.py", "tests/test_web3_access_control.py",
         "tests/test_web3_poc.py", "tests/test_verifiers_extended.py", "tests/test_coverage_unauth.py"]
rc, o, e = sh([PY, "-m", "pytest", "-q"] + tests)
line = [l for l in o.splitlines() if "passed" in l or "failed" in l]
out["capabilities"]["new_tool_tests"] = {"rc": rc, "summary": line[-1] if line else ""}

# 2) web3 PoC oracle live (needs forge + forge-std in the local lab)
w3 = {"available": os.path.isdir("/tmp/opencode/w3_lab/lib/forge-std")}
if w3["available"]:
    sys.path.insert(0, os.path.join(REPO, "bughunter"))
    from tools.verifiers.web3_poc import verify
    ok = verify({"vuln_class": "web3-poc", "project_dir": "/tmp/opencode/w3_lab", "test_name": "test_anyoneCanMint"})
    bad = verify({"vuln_class": "web3-poc", "project_dir": "/tmp/opencode/w3_lab", "test_name": "test_nope"})
    w3.update({"exploit_confirmed": bool(ok.confirmed), "absent_rejected": not bad.confirmed})
out["capabilities"]["web3_poc_oracle"] = w3

# 3) failure recovery: verifier on bad inputs must skip, not crash
sys.path.insert(0, os.path.join(REPO, "bughunter"))
from tools.verifiers import verify_finding
skips = [verify_finding({"vuln_class": "ssi"}), verify_finding({"vuln_class": "web3-poc"})]
out["capabilities"]["failure_recovery_skip"] = all(getattr(r, "skipped", False) for r in skips)

print(json.dumps(out, indent=2))
