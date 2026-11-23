#!/usr/bin/env python3
"""Cost-aware model router — cheap models for cheap stages, strong for reasoning.

Independent 2026 benchmarks converge: strong low-cost models are roughly tied
with frontier models per-task (Harness Matters, 2610.28802; AgentBreaker), and
the largest bill comes from routing *everything* through a frontier model. This
maps a hunt stage to a tier, picks the best available model in that tier, and
tracks cost so you can report $/solve.

    from tools.model_router import choose, CostLedger
    choose("recon")                 # -> a cheap model id
    choose("exploit_reasoning")     # -> a frontier model id
    led = CostLedger(); led.record("recon", "deepseek-v4-flash", 12000, 800)

CLI:
    python3 -m tools.model_router stage hunt
    python3 -m tools.model_router table
"""
from __future__ import annotations

import argparse
import json
import os

TIERS = ("cheap", "mid", "frontier")

STAGE_TIER = {
    "recon": "cheap",
    "parse": "cheap",
    "classify": "cheap",
    "app_model": "cheap",
    "rag": "cheap",
    "triage": "cheap",
    "dedupe": "cheap",
    "report": "mid",
    "validate": "mid",
    "falsify": "frontier",
    "exploit_reasoning": "frontier",
    "chain": "frontier",
    "planning": "frontier",
}

# Ordered preference per tier (first available wins).
TIER_MODELS = {
    "cheap": ["deepseek-v4-flash", "glm-5.3-flash", "qwen3.8-flash", "gpt-oss-20b",
              "llama3.3-70b"],
    "mid": ["claude-sonnet-4-6", "gemini-3.8-flash-high", "grok-4.3"],
    "frontier": ["claude-opus-4-8", "gpt-5.5", "deepseek-v4-pro", "grok-4.5"],
}

# USD per 1M tokens (input, output) — rough public list; override per deployment.
PRICES = {
    "deepseek-v4-flash": (0.28, 0.42),
    "glm-5.3-flash": (0.30, 0.60),
    "qwen3.8-flash": (0.35, 0.70),
    "gpt-oss-20b": (0.10, 0.30),
    "llama3.3-70b": (0.59, 0.79),
    "claude-sonnet-4-6": (3.0, 15.0),
    "gemini-3.8-flash-high": (0.50, 2.00),
    "grok-4.3": (2.0, 10.0),
    "claude-opus-4-8": (15.0, 75.0),
    "gpt-5.5": (10.0, 30.0),
    "deepseek-v4-pro": (0.60, 2.20),
    "grok-4.5": (5.0, 15.0),
}


def tier_for(stage: str) -> str:
    return STAGE_TIER.get((stage or "").lower(), "mid")


def choose(stage: str, *, available: list[str] | None = None,
           override: str | None = None) -> str:
    """Pick a model for `stage`. `available` restricts to what the env has."""
    if override:
        return override
    env_override = os.environ.get("BRAIN_MODEL")
    if env_override:
        return env_override
    tier = tier_for(stage)
    pool = TIER_MODELS[tier]
    if available:
        avail = {a.split("/")[-1] for a in available} | set(available)
        for m in pool:
            if m in avail or m.split("/")[-1] in avail:
                return m
    return pool[0]


def estimate_cost(model: str, in_tokens: int, out_tokens: int) -> float:
    pin, pout = PRICES.get(model, (1.0, 3.0))
    return (in_tokens / 1_000_000.0) * pin + (out_tokens / 1_000_000.0) * pout


class CostLedger:
    """Accumulate per-stage cost so a hunt can report $/solve."""

    def __init__(self):
        self.records: list[dict] = []

    def record(self, stage: str, model: str, in_tokens: int, out_tokens: int,
               *, solved: bool | None = None) -> float:
        cost = estimate_cost(model, in_tokens, out_tokens)
        self.records.append({
            "stage": stage, "model": model, "tier": tier_for(stage),
            "in_tokens": int(in_tokens), "out_tokens": int(out_tokens),
            "cost_usd": round(cost, 6), "solved": solved,
        })
        return cost

    @property
    def total_usd(self) -> float:
        return round(sum(r["cost_usd"] for r in self.records), 6)

    def per_solve(self, successes: int | None = None) -> float | None:
        if successes is None:
            successes = sum(1 for r in self.records if r.get("solved"))
        if not successes:
            return None
        return round(self.total_usd / successes, 6)

    def to_dict(self) -> dict:
        return {"schema": "cost-ledger/1", "total_usd": self.total_usd,
                "records": self.records}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Cost-aware model routing")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stage")
    s.add_argument("stage")
    s.add_argument("--available", nargs="*")
    s.add_argument("--json", action="store_true")
    sub.add_parser("table")
    args = ap.parse_args(argv)

    if args.cmd == "stage":
        model = choose(args.stage, available=args.available)
        out = {"stage": args.stage, "tier": tier_for(args.stage), "model": model,
               "price_per_1m": PRICES.get(model)}
        print(json.dumps(out, indent=2) if args.json
              else f"{args.stage}: {tier_for(args.stage)} -> {model}")
    else:
        table = {t: TIER_MODELS[t] for t in TIERS}
        print(json.dumps(table, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
