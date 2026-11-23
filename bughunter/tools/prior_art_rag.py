#!/usr/bin/env python3
"""Relevance-gated prior-art retrieval over the local knowledge corpus.

The SoK finding is blunt: naive retrieval over security corpora often *misleads*
agents — a superficially similar writeup drags the hunter onto the wrong bug
class. So this is deliberately small, offline, and gated:

  - pure-stdlib TF-IDF (no embeddings, no network, no model download)
  - a relevance gate: a hit must clear a score floor AND share >= N query terms
  - when nothing clears the gate it returns [] with `gated: True` (do not force
    "prior art" onto the agent)

    python3 -m tools.prior_art_rag search "s3 bucket takeover oauth" --top 5 --json
    python3 -m tools.prior_art_rag search "graphql idor" --dir knowledge --target acme.com
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_STOP = {
    "the", "and", "for", "with", "from", "that", "this", "are", "was", "were",
    "you", "your", "not", "but", "can", "how", "why", "when", "what", "into",
    "via", "use", "using", "一个", "the", "its", "it's", "has", "have", "had",
}
_TOKEN = re.compile(r"[a-z0-9_]{2,}")


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall((text or "").lower()) if t not in _STOP]


def _iter_docs(dirs: list[str], max_docs: int = 20000):
    """Yield (path, line_no_or_0, text) from md/txt/jsonl corpora."""
    seen = 0
    for root in dirs:
        if not os.path.isdir(root):
            continue
        for path in glob.glob(os.path.join(root, "**", "*"), recursive=True):
            if seen >= max_docs:
                return
            if not os.path.isfile(path):
                continue
            low = path.lower()
            if low.endswith((".md", ".txt")):
                try:
                    text = open(path, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                seen += 1
                yield path, 0, text
            elif low.endswith(".jsonl"):
                try:
                    for i, line in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
                        if seen >= max_docs:
                            return
                        line = line.strip()
                        if line:
                            seen += 1
                            yield path, i, line
                except OSError:
                    continue


def search(query: str, *, dirs: list[str] | None = None, top_k: int = 5,
           min_score: float = 0.12, min_overlap: int = 2,
           max_docs: int = 20000) -> dict:
    """Return {"query", "results": [...], "gated": bool, "reason": str}."""
    dirs = dirs or [os.path.join(REPO, "knowledge")]
    q_tokens = tokenize(query)
    if not q_tokens:
        return {"query": query, "results": [], "gated": True, "reason": "empty query"}

    docs: list[tuple[str, int, str, list[str], dict]] = []
    df: dict[str, int] = {}
    for path, line, text in _iter_docs(dirs, max_docs=max_docs):
        toks = tokenize(text)
        if not toks:
            continue
        tf: dict[str, int] = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        for t in tf:
            df[t] = df.get(t, 0) + 1
        docs.append((path, line, text, toks, tf))

    if not docs:
        return {"query": query, "results": [], "gated": True, "reason": "empty corpus"}

    n = len(docs)
    q_set = set(q_tokens)
    scored = []
    for path, line, text, toks, tf in docs:
        overlap = len(q_set & set(tf))
        if overlap < min(min_overlap, len(q_set)):
            continue
        score = 0.0
        norm = 0.0
        for t, c in tf.items():
            idf = math.log((n + 1) / (df.get(t, 0) + 1)) + 1.0
            w = (1.0 + math.log(c)) * idf
            norm += w * w
            if t in q_set:
                score += w * idf
        if norm:
            score = score / math.sqrt(norm)
        if score >= min_score:
            snippet = text.strip().replace("\n", " ")
            scored.append({
                "path": os.path.relpath(path, REPO),
                "line": line,
                "score": round(score, 4),
                "overlap": overlap,
                "snippet": snippet[:280],
            })

    scored.sort(key=lambda r: (r["score"], r["overlap"]), reverse=True)
    results = scored[:top_k]
    if not results:
        return {"query": query, "results": [], "gated": True,
                "reason": "no document cleared relevance gate (avoid misleading retrieval)"}
    return {"query": query, "results": results, "gated": False,
            "reason": f"{len(results)} relevant document(s)"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Relevance-gated prior-art retrieval (offline)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--dir", action="append", default=[])
    s.add_argument("--target", default="")
    s.add_argument("--top", type=int, default=5)
    s.add_argument("--min-score", type=float, default=0.12)
    s.add_argument("--min-overlap", type=int, default=2)
    s.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    dirs = args.dir or []
    if not dirs:
        dirs = [os.path.join(REPO, "knowledge")]
    if args.target:
        dirs.append(os.path.join(REPO, "findings", args.target))

    out = search(args.query, dirs=dirs, top_k=args.top, min_score=args.min_score,
                 min_overlap=args.min_overlap)
    if args.json:
        print(json.dumps(out, indent=2))
    elif out["gated"]:
        print(f"[gated] {out['reason']}")
    else:
        for r in out["results"]:
            loc = f":{r['line']}" if r["line"] else ""
            print(f"[{r['score']:.3f}] {r['path']}{loc}\n    {r['snippet'][:160]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
