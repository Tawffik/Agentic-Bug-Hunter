package cardano

import (
	"encoding/hex"
	"testing"

	ed255192 "github.com/okx/go-wallet-sdk/coins/cardano/ed25519"
)

// PoC: VerifyMessage accepts a signature made by an UNRELATED key as long as
// the caller supplies that unrelated key as both `key` and `publicKey`, while
// the `address` parameter is an arbitrary victim address. No binding between
// the signing public key and the address is ever checked.
func TestPoC_UnrelatedKeyAccepted(t *testing.T) {
	// Key A (victim) — taken from the upstream test vector.
	prvKeyA := "40e27cee4a8b4c4ec19e6e6060d78c1e0ecf18141df615b4d6294800b905425e511a28ae1a7595b8e9465b76f6cf4981238ac8be8584e767234fdca7f15e14d7c8fc0f836e5e7599d95cea1c9ac639c01b46ecf213ef7fe0af1804d7b905425e63d2f4e0b46a2c978c961ad55d5396a0f221e49cb004a26fbe422859fd77c5d1"

	addressA, err := NewAddressFromPrvKey(prvKeyA)
	if err != nil {
		t.Fatal(err)
	}

	// Key B — unrelated. Derive a different extended key by deriving from a mnemonic.
	prvKeyB, err := DerivePrvKey(
		"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
		"m/1852'/1815'/0'/0/0",
	)
	if err != nil {
		t.Fatal(err)
	}
	addressB, _ := NewAddressFromPrvKey(prvKeyB)
	if addressB == addressA {
		t.Fatal("keys unexpectedly identical")
	}
	t.Logf("victim address A         : %s", addressA)
	t.Logf("attacker address B       : %s", addressB)

	message := "1234"

	// Attacker signs with B, but asks the signer to claim address A in the header.
	res, err := SignMessage(prvKeyB, addressA, message)
	if err != nil {
		t.Fatal(err)
	}

	// The signing public key really is B's.
	pb, _ := hex.DecodeString(prvKeyB)
	pubB := []byte(ed255192.ExtendedPrivateKey(pb[:64]).Public().(ed255192.PublicKey))
	pubBHex := hex.EncodeToString(pubB)
	t.Logf("attacker pubkey (B)      : %s", pubBHex)

	// Sanity: signature was produced by B, over message, claiming address A.
	okNoAddr, _ := VerifyMessageNoAddr(res.Signature, res.Key, pubBHex, message)
	t.Logf("VerifyMessageNoAddr(B)   : %v (expected true — sig is genuinely B's)", okNoAddr)

	// THE BUG: verify as if it were an authentication by victim address A.
	verified, err := VerifyMessage(res.Signature, res.Key, pubBHex, addressA, message)
	t.Logf("VerifyMessage(B -> A)    : %v, err=%v", verified, err)

	if verified {
		t.Fatalf("VULNERABLE: unrelated key B accepted for address A (%s)", addressA)
	}
	t.Log("FIXED: unrelated key rejected")
}
