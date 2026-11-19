# Cardano `VerifyMessage` accepts signatures from an unrelated key — missing public-key↔address binding (authentication bypass)

## Summary

The `VerifyMessage` function in `coins/cardano/message.go` of `okx/go-wallet-sdk` verifies a signed-message (COSE Sign1) structure but never binds the signing public key to the Cardano address being claimed. Because the COSE header `address` is chosen freely at signing time, an attacker can sign a message with **any** key while declaring a **victim's** address, and `VerifyMessage` returns `true`. Any consumer that uses this to prove "the caller controls this address" (sign-in-with-wallet, ownership proof, session/auth issuance, withdrawal authorization) can be impersonated.

- **Repo (in scope):** `https://github.com/okx/go-wallet-sdk` — asset type `SOURCE_CODE`, bounty-eligible, max severity `critical` in the OKG HackerOne program (`https://hackerone.com/okg`)
- **Revision tested:** `89c5153f4669b0d81658b37bae902b62d495d574`
- **File:** `coins/cardano/message.go:124`
- **Function:** `VerifyMessage(signature, key, publicKey, address, message string) (bool, error)`
- **CWE-347:** Improper Verification of Cryptographic Signature
- **CVSS 3.1:** 9.1 (Critical) — `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`

## Vulnerability Details

`VerifyMessage` performs three checks, all against **caller-supplied** data:

| Line | Check |
|---|---|
| `message.go:171` | supplied COSE `key` matches supplied `publicKey` |
| `message.go:176` | header `address` equals the caller-supplied `address` parameter |
| `message.go:191` | the Ed25519 signature verifies under `publicKey` |

The `address` placed in the COSE protected header is set at signing time from a free parameter:

```go
// message.go:83-87  (SignMessageWithSigner)
headers := cose.Headers{
    Protected: cose.ProtectedHeader{
        cose.HeaderLabelAlgorithm: cose.AlgorithmEdDSA,
        "address":                 addr.Bytes(),   // caller-chosen
    },
    ...
}
```

Nothing in `VerifyMessage` recomputes the address from `publicKey` and compares it to the claimed address. The Blake2b-224 credential hash used to *build* addresses (`NewKeyCredential`, `credential.go:45`) is never used to *validate* them, so there is no key→address binding.

The sibling `VerifyMessageNoAddr` is, by name, the variant that deliberately skips the address check. `VerifyMessage`'s only additional purpose over it is the address check — which is broken.

## Steps to Reproduce

**Environment:** Go 1.23+, `github.com/okx/go-wallet-sdk/coins/cardano`

1. **Victim key A** (upstream test vector) → address A:
   `addr1q8nrdx6sukqwatkv7x8y0csl0x2l0rek9cmc04n5z35anxphyemygs8dxvfe432u6xcrt89d968u478w6s0cu8x7thrsng2ztx`
2. **Unrelated attacker key B** derived from
   mnemonic `abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about`, path `m/1852'/1815'/0'/0/0` → address B:
   `addr1qy8ac7qqy0vtulyl7wntmsxc6wex80gvcyjy33qffrhm7sh927ysx5sftuw0dlft05dz3c7revpf7jx0xnlcjz3g69mq4afdhv`
3. Sign with **B**, declaring **address A** in the header:
   ```go
   res, _ := SignMessage(prvKeyB, addressA, "1234")
   ```
4. Verify as if it were an authentication by victim address A:
   ```go
   verified, err := VerifyMessage(res.Signature, res.Key, pubBHex, addressA, "1234")
   ```

**Expected:** `false` — B does not control A.
**Actual:** `true, err=<nil>` — unrelated key accepted.

Observed PoC output:

```
victim address A   : addr1q8nrdx6sukqwatkv7x8y0csl0x2l0rek9cmc04n5z35anxphyemygs8dxvfe432u6xcrt89d968u478w6s0cu8x7thrsng2ztx
attacker address B : addr1qy8ac7qqy0vtulyl7wntmsxc6wex80gvcyjy33qffrhm7sh927ysx5sftuw0dlft05dz3c7revpf7jx0xnlcjz3g69mq4afdhv
attacker pubkey B  : 7ea09a34aebb13c9841c71397b1cabfec5ddf950405293dee496cac2f437480a
VerifyMessageNoAddr(B) : true   (sig is genuinely B's)
VerifyMessage(B -> A)  : true   <-- bypass
```

Confirming the fix: recomputing `Blake224Hash(pubKey[:32])` / `Blake224Hash(pubKey[32:])` and comparing to `addr.Payment.Hash()` / `addr.Stake.Hash()` correctly **rejects** B for A.

## Impact

Authentication / authorization bypass. Any wallet or backend that treats `VerifyMessage(...) == true` as "the caller controls `address`" is broken: an attacker authenticates as **any** Cardano address without its private key. Affects sign-in-with-wallet, ownership proofs, session/token issuance, and withdrawal/transfer authorization built on this SDK. No privileges or user interaction required.

## Recommended Fix

In `VerifyMessage` (around `message.go:176`), recompute the address from the signing key and require it to match before `msg.Verify`:

```go
payHash, _ := Blake224Hash(pubKey[:32])
stakeHash, _ := Blake224Hash(pubKey[32:])
if !bytes.Equal(addr.Payment.Hash(), payHash) || !bytes.Equal(addr.Stake.Hash(), stakeHash) {
    return false, errors.New("signing key does not match address")
}
```

(For enterprise/pointer addresses, compare the payment credential only.)

## Supporting Materials

- `evidence/poc_test.go` — exploit test (`TestPoC_UnrelatedKeyAccepted`), fails on vulnerable revision
- `evidence/poc_fix_test.go` — binding check rejects the attacker key
- PoC location: `/tmp/opencode/gws/coins/cardano/`
