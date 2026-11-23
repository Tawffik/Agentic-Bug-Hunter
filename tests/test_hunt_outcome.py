"""Tests for tools/hunt_outcome.py — outcome root-cause classifier."""

import json
import os

from tools.hunt_outcome import analyze, classify_reason, main


def _lead(status, note="", skill="hunt-idor", priority="high"):
    return {"id": "lb-x", "target": "t", "skill": skill, "priority": priority,
            "evidence": "https://t/x?id=1", "status": status, "note": note}


def test_classify_reason_buckets():
    assert classify_reason("needs manual input: session required") == "auth"
    assert classify_reason("user is not logged in") == "auth"
    assert classify_reason("no verifier for hunt-foo") == "no_verifier"
    assert classify_reason("no deterministic verifier for hunt-foo") == "no_verifier"
    assert classify_reason("oracle fired; chain required before report") == "chain"
    assert classify_reason("") == "other"


def test_auth_wins_over_chain():
    # A note mentioning both must land in the more actionable bucket.
    assert classify_reason("chain required; also needs session") == "auth"


def test_no_data():
    out = analyze("ghost", leads=[], findings_dirs=["/nonexistent"])
    assert out["verdict"] == "no_data"
    assert out["next_actions"] == []


def test_unattempted_leads_is_top_cause():
    leads = [_lead("new"), _lead("new"), _lead("killed")]
    out = analyze("t", leads=leads, findings_dirs=["/nonexistent"])
    assert out["verdict"] == "unattempted_leads"
    assert out["counts"]["new"] == 2
    assert any(c["code"] == "unattempted_leads" for c in out["causes"])
    assert any("swarm" in a for a in out["next_actions"])


def test_auth_blocked_when_no_new_leads():
    leads = [_lead("parked", "needs manual input: session required"),
             _lead("parked", "403 permission error")]
    out = analyze("t", leads=leads, findings_dirs=["/nonexistent"])
    assert out["verdict"] == "auth_blocked"
    assert out["parked_buckets"]["auth"] == 2


def test_hardened_when_all_killed():
    leads = [_lead("killed", "verifier rejected: xss"), _lead("killed")]
    out = analyze("t", leads=leads, findings_dirs=["/nonexistent"])
    assert out["verdict"] == "hardened"


def _write_validation(root, target, rel, payload):
    d = os.path.join(root, target, rel)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "validation.json"), "w") as fh:
        json.dump(payload, fh)
    return d


def test_report_ready_unsubmitted_beats_unattempted(tmp_path):
    findings = str(tmp_path)
    _write_validation(findings, "t", "swarm/lb-1", {
        "status": "validated_finding", "technically_confirmed": True,
        "contract_required": True, "contract_satisfied": True,
        "verifier": {"confirmed": True, "skipped": False},
    })
    leads = [_lead("new")]  # there are also untouched leads
    out = analyze("t", leads=leads, findings_dirs=[findings])
    assert out["verdict"] == "report_ready_unsubmitted"
    assert out["report_ready"] == 1
    assert any(c["code"] == "report_ready_unsubmitted" for c in out["causes"])


def test_report_ready_with_draft_is_not_a_miss(tmp_path):
    findings = str(tmp_path)
    _write_validation(findings, "t", "swarm/lb-1", {
        "status": "validated_finding", "technically_confirmed": True,
        "verifier": {"confirmed": True, "skipped": False},
    })
    with open(os.path.join(findings, "t", "hackerone-report.md"), "w") as fh:
        fh.write("# report")
    out = analyze("t", leads=[_lead("investigating")], findings_dirs=[findings])
    assert out["report_ready"] == 1
    assert out["report_draft"] is True
    assert out["verdict"] != "report_ready_unsubmitted"


def test_cli_json_and_exit_codes(tmp_path, capsys):
    leads_dir = tmp_path / "leads"
    leads_dir.mkdir()
    with open(os.path.join(str(leads_dir), "t.jsonl"), "w") as fh:
        fh.write(json.dumps(_lead("parked", "no verifier for hunt-foo")) + "\n")

    rc = main(["t", "--leads-dir", str(leads_dir),
               "--findings-dir", str(tmp_path / "none"), "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["verdict"] == "capability_gap"

    # No data at all -> exit 2
    empty = tmp_path / "empty"
    empty.mkdir()
    rc2 = main(["ghost", "--leads-dir", str(empty),
                "--findings-dir", str(tmp_path / "none")])
    assert rc2 == 2
