#!/usr/bin/env python3
"""Program intel + target score for a single bounty program.

Pulls public stats only:
  - HackerOne: public GraphQL team stats/policy
  - Bugcrowd: public engagement statistics JSON

Outputs a 0-100 planning score and a JSON snapshot. The score is a
prioritisation aid, not a prediction of payout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

H1_GRAPHQL = "https://hackerone.com/graphql"
BUGCROWD_STATS = "https://bugcrowd.com/engagements/{handle}/statistics"
UA = "agentic-bug-hunter/program-intel"


def _request(url: str, data: bytes | None = None, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA,
        "Accept": "application/json",
        **(headers or {}),
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_hackerone(handle: str) -> dict:
    query = """{
      team(handle: "%s") {
        name handle url offers_bounties currency base_bounty
        resolved_report_count average_bounty_lower_amount average_bounty_upper_amount
        launched_at state
      }
    }""" % handle.replace('"', "")
    payload = json.dumps({"query": query}).encode()
    data = _request(H1_GRAPHQL, payload, {"Content-Type": "application/json"})
    team = (data.get("data") or {}).get("team")
    if not team:
        raise RuntimeError(f"HackerOne program not found: {handle}")
    return {
        "platform": "hackerone",
        "handle": team.get("handle", handle),
        "name": team.get("name", ""),
        "url": team.get("url", f"https://hackerone.com/{handle}"),
        "offers_bounties": bool(team.get("offers_bounties")),
        "currency": (team.get("currency") or "usd").upper(),
        "base_bounty": team.get("base_bounty") or 0,
        "avg_bounty_lower": team.get("average_bounty_lower_amount") or 0,
        "avg_bounty_upper": team.get("average_bounty_upper_amount") or 0,
        "resolved_reports": team.get("resolved_report_count") or 0,
        "launched_at": (team.get("launched_at") or "")[:10],
        "state": team.get("state", ""),
    }


def parse_money(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").replace(",", "")
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)
    return float(match.group(1)) if match else 0.0


def fetch_bugcrowd(handle: str) -> dict:
    data = _request(BUGCROWD_STATS.format(handle=urllib.parse.quote(handle)))
    return {
        "platform": "bugcrowd",
        "handle": handle,
        "name": handle,
        "url": f"https://bugcrowd.com/engagements/{handle}",
        "offers_bounties": True,
        "currency": "USD",
        "base_bounty": 0,
        "avg_bounty_lower": 0,
        "avg_bounty_upper": parse_money(data.get("averagePayout")),
        "resolved_reports": int(data.get("rewardedVulnerabilities") or 0),
        "validation": data.get("validationWithin") or "",
        "state": "open",
    }


def score_program(program: dict) -> int:
    """0-100 planning score: payout, activity, freshness, validation speed."""
    score = 0.0
    top = max(parse_money(program.get("avg_bounty_upper")), parse_money(program.get("base_bounty")))
    if top >= 10000:
        score += 40
    elif top >= 5000:
        score += 30
    elif top >= 2000:
        score += 20
    elif top >= 500:
        score += 10
    resolved = int(program.get("resolved_reports") or 0)
    score += min(20, resolved / 10)
    if program.get("offers_bounties"):
        score += 10
    launched = program.get("launched_at") or ""
    if launched:
        try:
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(launched + "T00:00:00+00:00")).days
            if age < 180:
                score += 15
            elif age < 365:
                score += 10
            elif age < 730:
                score += 5
        except ValueError:
            pass
    validation = str(program.get("validation") or "")
    if "day" in validation.lower():
        try:
            days = int(re.search(r"(\d+)", validation).group(1))
            if days <= 2:
                score += 15
            elif days <= 7:
                score += 10
            elif days <= 14:
                score += 5
        except Exception:
            pass
    if program.get("state", "").lower() in {"open", "public_mode", "in_progress"}:
        score += 5
    return max(0, min(100, round(score)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Public program stats + 0-100 target score.")
    parser.add_argument("--platform", required=True, choices=["hackerone", "bugcrowd"])
    parser.add_argument("--handle", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", default="memory/program-intel", help="Snapshot directory")
    args = parser.parse_args(argv)

    try:
        if args.platform == "hackerone":
            program = fetch_hackerone(args.handle)
        else:
            program = fetch_bugcrowd(args.handle)
    except (urllib.error.URLError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    program["score"] = score_program(program)
    program["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{args.platform}-{args.handle}.json").write_text(
        json.dumps(program, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(program, indent=2))
        return 0

    print(f"{program.get('name') or args.handle} ({args.platform}:{args.handle})")
    print(f"  score:       {program['score']}/100")
    print(f"  bounty top:  {max(parse_money(program.get('avg_bounty_upper')), parse_money(program.get('base_bounty'))):,.0f} {program.get('currency','')}")
    print(f"  resolved:    {program.get('resolved_reports', 0)}")
    print(f"  launched:    {program.get('launched_at') or 'unknown'}")
    print(f"  state:       {program.get('state') or 'unknown'}")
    snapshot = out / f"{args.platform}-{args.handle}.json"
    print(f"  snapshot:    {snapshot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
