---
description: Validate and ingest a BugBountyCI/Agentic lifecycle handoff into the lead board. Usage: /handoff-ingest <agent-handoff-dir> [--ingest]
---

# /handoff-ingest

```bash
python3 bughunter/tools/handoff_ingest.py path/to/agent-handoff --ingest
```

Validates `schemas/lifecycle.schema.json` fields, dedupes/ranks leads, and adds
them to the per-target lead board. Read-only unless `--ingest` is passed.
