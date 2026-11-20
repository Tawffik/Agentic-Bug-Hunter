# Upstream attribution — web3-fuzz

This skill is adapted from **Pashov Audit Group Skills — fizz**:
https://github.com/pashov/skills/tree/main/fizz

Upstream license: MIT (Copyright (c) 2024 AI Skills Contributors).

What was imported:
- `templates/` (fuzz harness scaffold and utility libraries)
- `references/` (selection, setup, handler, property, template-map)
- `scripts/` (ABI extraction, function selection, suite/handler generation,
  Medusa/Echidna runners, fuzz-profile helper)
- `agents/` (invariant-discovery and report prompts)

What was changed:
- A harness-neutral `SKILL.md` with explicit lead-only, coverage, and PoC rules.
- Tool checks use the repo's `install_tools.sh --with-web3` and
  `bughunter/tools/chain_audit_env.sh`.
- Claude-specific model routing and interactive UI language were removed; the
  scripts and templates are unchanged and remain MIT-licensed.

Keep this file and the upstream MIT notice when redistributing.
