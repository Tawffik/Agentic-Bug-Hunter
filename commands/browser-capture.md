---
description: Capture an authenticated SPA session with Playwright — network requests, storage, cookies, screenshot, HAR, storage state. Usage: /browser-capture <url> [--storage-state auth.json]
---

# /browser-capture

Use `bughunter/tools/browser_capture.py` to map an authenticated browser
session before sending requests to the IDOR/auth/API tools.

```bash
python3 bughunter/tools/browser_capture.py "$URL" \
  --storage-state auth.json --har --out captures/target
```

Read-only: loads the page, does not submit forms or sign transactions. Keep
`--storage-state-out` files private; they contain session secrets.
