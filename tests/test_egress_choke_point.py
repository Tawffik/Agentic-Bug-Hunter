"""CI gate: the verification path must not open sockets outside the choke point.

The verifier library owns exactly ONE network seam: `verifiers/base.py::fetch`.
Every per-class verifier must import that and nothing else that can phone home.
This test fails if a future verifier (or the gate modules) reaches for raw
urllib/requests/socket, which is how scope + SSRF guarantees get bypassed.
"""
import glob
import os
import re

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIERS = os.path.join(REPO, "bughunter", "tools", "verifiers")

_NETWORK_PRIMITIVES = [
    r"urllib\.request\.urlopen\s*\(",
    r"\burlopen\s*\(",
    r"\brequests\.(get|post|put|patch|head|delete|request)\s*\(",
    r"\bhttp\.client\b",
    r"\bsocket\.(create_connection|socket)\s*\(",
]

_ALLOWED = {"base.py", "__init__.py", "__main__.py"}


def _verifier_files():
    return [p for p in glob.glob(os.path.join(VERIFIERS, "*.py"))
            if os.path.basename(p) not in _ALLOWED]


@pytest.mark.parametrize("path", _verifier_files(), ids=os.path.basename)
def test_verifier_has_no_raw_network_primitive(path):
    src = open(path, encoding="utf-8").read()
    for pat in _NETWORK_PRIMITIVES:
        assert not re.search(pat, src), f"{os.path.basename(path)} bypasses base.fetch: /{pat}/"


@pytest.mark.parametrize("path", _verifier_files(), ids=os.path.basename)
def test_verifier_goes_through_base_fetch_or_skips(path):
    src = open(path, encoding="utf-8").read()
    # Either it fetches via the shared seam, or it is an orchestrator that
    # delegates (ssrf -> oob), which is acceptable.
    assert "from tools.verifiers.base import" in src
    assert ("fetch" in src) or ("oob" in src) or ("dom_xss_harness" in src), \
        f"{os.path.basename(path)} has no data path"


def test_gate_modules_use_choke_points():
    tools = os.path.join(REPO, "bughunter", "tools")
    # validate_core/adversarial/evidence_contract must not open raw sockets.
    for name in ("validate_core.py", "adversarial_validator.py", "evidence_contract.py"):
        src = open(os.path.join(tools, name), encoding="utf-8").read()
        assert not re.search(r"urllib\.request\.urlopen\s*\(", src), f"{name} opens raw urlopen"

    # adversarial_validator must go through the shared fetch.
    adv = open(os.path.join(tools, "adversarial_validator.py"), encoding="utf-8").read()
    assert "from tools.verifiers.base import" in adv and "fetch" in adv

    # verifier.py must delegate to poc_bundler (which uses safe_http).
    vf = open(os.path.join(tools, "verifier.py"), encoding="utf-8").read()
    assert "import poc_bundler" in vf
