"""Enforce that every unauth niche class has skill-corpus coverage."""

import glob
import re

CORPUS = "\n".join(open(f, errors="replace").read() for f in glob.glob("skills/**/*.md", recursive=True))

CLASSES = {
    "SSI Injection": r"ssi injection|server.side includes",
    "XPath Injection": r"xpath injection",
    "Client-Side Path Traversal": r"client.side path traversal",
    "ORM Leak": r"orm leak",
    "Email Header Injection": r"email header injection",
    "Insecure Randomness": r"insecure randomness",
    "XS-Leak": r"xs-leak|xsleak",
}


def test_all_unauth_niche_classes_covered():
    missing = [k for k, p in CLASSES.items() if not re.search(p, CORPUS, re.I)]
    assert not missing, f"uncovered classes: {missing}"
