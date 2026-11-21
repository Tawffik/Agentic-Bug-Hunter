# Knowledge corpus

Reference material that is **not** a loadable skill but is searched by the
agent during a hunt.

## `tips/`

333 standalone bug-bounty tips exported from the Notion *Bug Bounty Tips &
Tricks* database, each with the original execution contract.

- `INDEX.md` — title → file index
- `CATEGORIES.md` — category counts
- `skills/` — one Markdown file per tip
- `by-category/` — category indexes
- `data/tips.json` — machine-readable source
- `LICENSE` — MIT (upstream)

Use it as a checklist/search surface, not as a scanner: pick a tip, map it to
the current target, and prove the trigger before reporting.

## `notion/`

Standalone Notion skill sources consolidated from the `bb-*` repos; see
`INDEX.md` for the mapping.
