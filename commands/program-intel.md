---
description: Pull public bounty-program stats and compute a 0-100 target score. Usage: /program-intel hackerone:okg or /program-intel bugcrowd:aiven-mbb-og
---

# /program-intel

```bash
python3 bughunter/tools/program_intel.py --platform hackerone --handle okg
python3 bughunter/tools/program_intel.py --platform bugcrowd --handle aiven-mbb-og
```

Prints a score and writes `memory/program-intel/<platform>-<handle>.json`.
Public stats only; still read the program page and known issues before hunting.
