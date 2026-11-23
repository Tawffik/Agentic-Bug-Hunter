"""Tests for tools/planning_ledger.py — explicit commitment state."""

import json

from tools import planning_ledger as pl


def test_add_is_idempotent_while_held(tmp_path):
    d = str(tmp_path)
    a = pl.add("acme.com", "order id is sequential and unowned", vuln_class="idor", directory=d)
    b = pl.add("acme.com", "order id is sequential and unowned", directory=d)
    assert a["id"] == b["id"]
    assert len(pl.load("acme.com", directory=d)) == 1


def test_touch_converts_and_removes_from_open(tmp_path):
    d = str(tmp_path)
    rec = pl.add("acme.com", "s3 bucket is writable", directory=d)
    assert pl.next_for("acme.com", directory=d)["id"] == rec["id"]
    pl.touch("acme.com", rec["id"], "converted", note="validated", directory=d)
    assert pl.list_open("acme.com", directory=d) == []
    assert pl.summary("acme.com", directory=d)["counts"]["converted"] == 1


def test_touch_unknown_returns_none(tmp_path):
    assert pl.touch("acme.com", "H-nope", "killed", directory=str(tmp_path)) is None


def test_invalid_status_raises(tmp_path):
    import pytest
    rec = pl.add("acme.com", "x hypothesis", directory=str(tmp_path))
    with pytest.raises(ValueError):
        pl.touch("acme.com", rec["id"], "bogus", directory=str(tmp_path))


def test_next_prefers_high_confidence(tmp_path):
    d = str(tmp_path)
    pl.add("acme.com", "low one", confidence="low", directory=d)
    hi = pl.add("acme.com", "high one", confidence="high", directory=d)
    assert pl.next_for("acme.com", directory=d)["id"] == hi["id"]


def test_stale_returns_old_held(tmp_path):
    d = str(tmp_path)
    rec = pl.add("acme.com", "stale hypothesis", directory=d)
    path = pl.ledger_path("acme.com", directory=d)
    rec["created"] = "2020-01-01T00:00:00+00:00"
    rec["updated"] = "2020-01-01T00:00:00+00:00"
    open(path, "w").write(json.dumps(rec) + "\n")
    assert pl.stale(24, "acme.com", directory=d)
