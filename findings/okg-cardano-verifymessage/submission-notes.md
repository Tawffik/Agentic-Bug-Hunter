# Submission Notes — OKG / okx/go-wallet-sdk Cardano VerifyMessage

## Program / scope verification

- Program: **OKG** — `https://hackerone.com/okg`
- In-scope asset (confirmed via HackerOne program scope): `https://github.com/okx/go-wallet-sdk` — `SOURCE_CODE`, `eligible_for_bounty = true`, `max_severity = critical`
- Note: the org-only asset `https://github.com/okx` is **out of scope**; this finding is on the specific in-scope repo, which is listed separately.
- Scope source: HackerOne program data (`okg`), plus repo `SECURITY.md` which points to the `okg` H1 program.

## Status

- [x] Scope confirmed (in scope — exact repo listed)
- [x] Root cause identified (`message.go:124` `VerifyMessage`, missing pubkey↔address binding)
- [x] PoC executed and passing on revision `89c5153f4669b0d81658b37bae902b62d495d574`
- [x] Fix verified (binding check rejects attacker key)
- [ ] Awaiting researcher to submit via HackerOne

## Pre-submit checklist

- [x] Title follows formula: [Class] in [endpoint] allows [actor] to [impact]
- [x] First sentence states exact impact
- [x] Steps to reproduce copy-paste ready
- [x] Response/proof of the bug included (PoC output)
- [x] Distinct keys used (A vs B) — not one account testing itself
- [x] CVSS 3.1 calculated and included
- [x] Recommended fix is concrete
- [x] No theoretical "could potentially" language

## CVSS

`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` = **9.1 (Critical)**

Library-level: final severity depends on how downstream consumers use the address check. Frame impact as authentication bypass; downgrade counter if triager argues "library only": the SDK's own `SECURITY.md` invites security reports and the function's documented purpose is address-ownership verification.

## Downgrade counters

| Program might say | Counter |
|---|---|
| "Library, not a live service" | It is an in-scope SOURCE_CODE asset; consumers relying on `VerifyMessage` for address ownership get a full auth bypass. |
| "Requires the verifier to pass the attacker key" | The API signature takes `key`/`publicKey` from the same untrusted message bundle a client submits; the check exists precisely to stop this and does not. |
| "`VerifyMessageNoAddr` exists for a reason" | `VerifyMessage`'s only meaningful addition over `NoAddr` is the address check; that check is non-functional. |

## References

- `coins/cardano/message.go` — `VerifyMessage` (line 124), `SignMessageWithSigner` (line 72), header `address` set at line 86
- `coins/cardano/credential.go:45` — `NewKeyCredential` (Blake2b-224 of pubkey; the binding that is never checked)
- `coins/cardano/account.go` — `NewAddressFromPrvKey`, `NewAddressFromPubKey`
- `coins/cardano/message_test.go` — upstream `TestVerifyMessage` (uses self-consistent inputs, so it never exercises the cross-key case)

## Next action

Submit `hackerone-report.md` to `https://hackerone.com/okg` on the `https://github.com/okx/go-wallet-sdk` asset.
