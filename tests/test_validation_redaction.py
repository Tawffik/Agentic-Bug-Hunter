import json
from tools.validate_core import verify_finding_programmatic

def test_programmatic_validation_redacts_identity_headers(tmp_path):
    finding = {
        "vuln_class": "idor",
        "victim_object_url": "http://127.0.0.1:1/closed",
        "attacker_headers": {"Cookie": "sess=SUPERSECRET", "Authorization": "Bearer TOPSECRET"},
        "victim_marker": "victim@example.test",
        "target": "127.0.0.1",
    }
    verify_finding_programmatic(finding, write_dir=str(tmp_path), log_research=False)
    text = (tmp_path / "validation.json").read_text()
    assert "SUPERSECRET" not in text and "TOPSECRET" not in text
    assert "victim@example.test" not in text
