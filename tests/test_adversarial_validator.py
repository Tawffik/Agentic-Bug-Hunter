"""Tests for tools/adversarial_validator.py — offline, via an injected fetcher."""

import json

from tools.adversarial_validator import falsify


def _fetcher(mapping):
    """mapping: url -> (status, body). Missing url -> (404, '')."""
    def _f(url, headers=None, method="GET", data=None):
        return mapping.get(url, (404, ""))
    return _f


def test_public_marker_is_falsified():
    f = {"vuln_class": "idor", "url": "https://t/obj?id=2",
         "victim_marker": "victim@x"}
    r = falsify(f, fetcher=_fetcher({"https://t/obj?id=2": (200, "victim@x")}))
    assert r["verdict"] == "FALSIFIED"
    assert any("public" in x for x in r["reasons"])


def test_generic_baseline_marker_is_falsified():
    f = {"vuln_class": "xss", "url": "https://t/a", "baseline_url": "https://t/home",
         "success_marker": "WELCOME"}
    r = falsify(f, fetcher=_fetcher({"https://t/a": (200, "nothing"),
                                     "https://t/home": (200, "WELCOME")}))
    assert r["verdict"] == "FALSIFIED"
    assert any("baseline" in x for x in r["reasons"])


def test_own_object_marker_is_falsified():
    f = {"vuln_class": "idor", "victim_object_url": "https://t/obj?id=2",
         "attacker_object_url": "https://t/obj?id=1",
         "attacker_headers": {"Authorization": "A"}, "victim_marker": "victim@x"}
    r = falsify(f, fetcher=_fetcher({
        "https://t/obj?id=2": (403, "denied"),
        "https://t/obj?id=1": (200, "victim@x"),  # same data as "victim"
    }))
    assert r["verdict"] == "FALSIFIED"
    assert any("cross-tenant" in x for x in r["reasons"])


def test_login_page_echo_is_falsified():
    f = {"vuln_class": "auth-bypass", "url": "https://t/admin",
         "success_marker": "Admin Panel"}
    r = falsify(f, fetcher=_fetcher({
        "https://t/admin": (200, "Please log in. Admin Panel"),
    }))
    assert r["verdict"] == "FALSIFIED"
    assert any("login" in x for x in r["reasons"])


def test_clean_control_survives():
    f = {"vuln_class": "idor", "victim_object_url": "https://t/obj?id=2",
         "attacker_object_url": "https://t/obj?id=1",
         "attacker_headers": {"Authorization": "A"}, "victim_marker": "victim@x"}

    def fetcher(url, headers=None, method="GET", data=None):
        authed = bool(headers and headers.get("Authorization"))
        if url.endswith("id=2"):
            return (200, "victim@x") if authed else (403, "denied")
        if url.endswith("id=1"):
            return (200, "attacker@y")
        return (404, "")

    r = falsify(f, fetcher=fetcher)
    assert r["verdict"] == "SURVIVES"


def test_no_marker_is_inconclusive():
    r = falsify({"vuln_class": "xss", "url": "https://t/x"})
    assert r["verdict"] == "INCONCLUSIVE"


def test_network_failure_is_inconclusive_not_pass():
    def boom(url, headers=None, method="GET", data=None):
        raise TimeoutError("nope")
    f = {"vuln_class": "idor", "victim_object_url": "https://t/obj?id=2",
         "victim_marker": "victim@x"}
    r = falsify(f, fetcher=boom)
    assert r["verdict"] == "INCONCLUSIVE"
