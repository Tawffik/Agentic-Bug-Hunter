---
description: Ingest an OpenAPI 3.x / Swagger 2.0 / Postman collection into the API attack surface and route every declared endpoint to a hunt-* skill. Usage: /spec-ingest <spec-file> --target <host> [--ingest]
---

# /spec-ingest

Test the API from its **contract**, not just what a crawler found. Every declared
endpoint becomes a classified lead on the lead board.

```bash
# Preview the endpoints + routing (no writes to the board):
python3 bughunter/tools/spec_ingest.py openapi.yaml --target api.example.com

# Route distinct leads to the persistent lead board:
python3 bughunter/tools/spec_ingest.py api-spec.json --target api.example.com --ingest

# Machine-readable summary:
python3 bughunter/tools/spec_ingest.py postman_collection.json --target api.example.com --json
```

Supports OpenAPI 3.x, Swagger 2.0 and Postman v2 collections (JSON or YAML).

What it routes:

| Signal | Lead |
|:---|:---|
| `{id}` / `userId` / `order_id` path or query params | `hunt-idor` |
| `url`/`callback`/`redirect`/`next` query params | `hunt-ssrf`, `hunt-open-redirect` |
| `/admin`/`/internal`/`/actuator` paths | `hunt-auth-bypass` |
| `upload`/`files`/`avatar` paths or params | `hunt-file-upload` |
| login/token/otp/reset paths | `hunt-oauth`, `hunt-ato` |
| `POST/PUT/PATCH/DELETE` with no declared `security` | `hunt-api-misconfig` |
| chat/completions/mcp paths | `hunt-llm-ai` |

Output is written to `recon/<target>/api/spec_endpoints.txt` and
`recon/<target>/api/spec_findings.json`. LEAD-only — it never sends a request.

The `/hunt` pipeline calls this automatically after recon when a spec file is
present under `recon/<target>/`.
