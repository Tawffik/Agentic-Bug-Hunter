# Verifier Benchmark

Measures the deterministic verifier gate (`tools/verifiers/` + `bughunter/tools/validate_core.py`)
the way XBOW measures itself: with ground-truth targets and a canary oracle, so a
"solve" can never be fabricated.

## What it measures

| Metric | Target | Meaning |
|---|---|---|
| recall | 1.0 | every live bug is deterministically confirmed |
| precision | 1.0 | nothing confirmed that isn't real |
| fp_rate / FP | 0 | **no unverified finding reaches report** |

## Targets

- **`vuln_target.py`** — intentionally vulnerable app (recall). Each run plants a
  unique `FLAG{random}` (XBOW canary pattern); the sensitive-file / IDOR / auth
  cases only count when the exploit exfiltrates that exact flag, so a confirm
  cannot be faked. Bugs: open redirect, `.env` leak, time- and error-based SQLi,
  IDOR (two-identity), auth bypass.
- **`demo/app.py` (hardened)** — precision / true-negative target. All 6 tutorial
  bugs are fixed, so any confirm here is a false positive. `demo.py` asserts it
  stays hardened.

## Run it

```bash
python3 tests/benchmark/score.py            # scoreboard; exits non-zero on FP or recall<1
python3 tests/benchmark/score.py --json
python3 tests/benchmark/demo.py             # assert the shipped demo is hardened
pytest tests/test_benchmark.py -q           # CI smoke test

python3 tests/benchmark/authz_score.py      # two-identity IDOR/BOLA discovery + confirmation
pytest tests/test_authz_benchmark.py -q     # CI smoke test for authz differential
```

### Authz differential benchmark

`authz_score.py` boots a two-user target with one real cross-tenant BOLA and six
authorization controls (`/api/me` per-user, shared team object, enforced admin,
public status, HTML shell, A-denied baseline). It scores:

- **recall** — the real BOLA is confirmed by the deterministic IDOR verifier
- **confirmed_fp** — no safe endpoint is confirmed
- **marker_lead_fp** — no safe endpoint is classified `CROSS_USER_MARKER`
- **verdict_accuracy** — every control maps to its intended verdict

Current baseline: recall 1.0, confirmed_fp 0, marker_lead_fp 0, verdict_accuracy 1.0.

## External suites (opt-in — not in CI)

The internal benchmark is a regression floor, not a competitive leaderboard.
For breadth, point the tool at public labs:

- **XBOW validation-benchmarks** (104 Dockerized CTFs, Apache-2.0):
  <https://github.com/xbow-engineering/validation-benchmarks>. Each container
  injects a fresh `FLAG{...}` at build time — a solve only counts when the live
  target emits that flag. NOTE: the repo's own README warns these are saturated
  (~100% industry pass as of 2026), so treat them as a smoke test / regression
  floor, not a discriminator.
- **PortSwigger Web Security Academy** labs (free): broad, per-class coverage.
- **PentesterLab**: additional breadth.

To avoid training-data contamination (the reason the XBOW 104 saturated), build
your own private, never-published novel set and keep it out of git.

## Adding a case

Edit `cases.py`: add to `recall_cases()` (vulnerable, must confirm) or
`precision_cases()` (hardened, must not). A recall case that asserts secret
content should key on the per-run `flag` so the oracle is canary-backed.
