# OKG Recon Results — okx.com / oklink.com

**Date:** 2026-11-08
**Scope (OKG, https://hackerone.com/okg):** `*.okx.com`, `*.oklink.com` (both in scope, bounty-eligible, max_severity critical)
**Method:** passive subdomain enumeration + live host probing only. No exploitation.

## Summary

| Stage | Tool | Count |
|---|---|---|
| Subdomains (okx.com) | subfinder | 552 |
| Subdomains (oklink.com) | subfinder | 22 |
| Total unique subdomains | — | 574 |
| Live hosts (HTTP/HTTPS) | httpx | 58 |

## Files

- `okx.subs.txt` — passive subdomains for `okx.com`
- `oklink.subs.txt` — passive subdomains for `oklink.com`
- `all.subs.txt` — combined, unique
- `httpx.txt` — live hosts with status code + title + tech (ANSI stripped)

## Live host highlights

| Host | Status | Notes |
|---|---|---|
| `okctools.okx.com` | 200 | "OKTC Safe" tool — interactive surface |
| `oktcsafe.okx.com` | 200 | "OKTC Safe" tool — interactive surface |
| `web3.okx.com` | 200 | OKX Wallet / onchain OS |
| `www.oklink.com` | 200 | blockchain explorer (GeeTest present) |
| `www.okx.com` / `app.okx.com` | 302 | main app |
| `chainrpc.okx.com` | 501 | JSON-RPC node endpoint |
| `xlayerrpc.okx.com` | 405 | XLayer RPC (method not allowed → POST-only) |
| `xlayertestrpc.okx.com` | 405 | XLayer testnet RPC |
| `xlayertestws.okx.com` | 400 | XLayer testnet WS |
| `xlayerws.okx.com` | 400 | XLayer WS |
| `*travelrule.okx.com` | 403 | travel-rule APIs (EEA/US) |
| `link.okx.com` | 403 | |
| `file.okx.com` / `static.okx.com` | 403 | CDN / object storage (Alibaba, CloudFront) |
| `static.oklink.com` | 302 | Alibaba OSS |
| `pay.okx.com` / `payauth.okx.com` | 403 | payment + auth (Cloudflare challenge) |
| `oklink.com` | 301 | apex redirect |

Tech stack observed: Cloudflare (Bot Management on nearly everything), Alibaba Cloud OSS, Amazon CloudFront, Google Cloud CDN, Tengine, HSTS, HTTP/3.

## Triage notes (do NOT test on live Okx services)

- Nearly all hosts sit behind **Cloudflare Bot Management** — aggressive testing risks IP block and is not covered by most OKG rules for automated scanning.
- OKG explicitly excludes: `*.okg.com`, `okx.ai`, `https://web3.okx.com/onchainos`, testnet faucets/testnets, and the org `https://github.com/okx`.
- Highest-signal candidates for **manual** review (still within scope, low-noise):
  - `chainrpc.okx.com` / `xlayerrpc.okx.com` — JSON-RPC surfaces (method enumeration, batch limits) — manual only.
  - `okctools.okx.com` / `oktcsafe.okx.com` — interactive tools with 200 responses.
  - `travelrule.okx.com` variants — regulatory APIs, 403-gated.
- No exploitation was performed in this recon pass.

## Scope cross-check

Both wildcards were verified in-scope. The recon only resolved hosts under `okx.com` and `oklink.com`, so every enumerated asset is covered by the OKG scope (subject to path/feature exclusions above).
