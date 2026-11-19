package cardano

import (
	"bytes"
	"encoding/hex"
	"testing"

	ed255192 "github.com/okx/go-wallet-sdk/coins/cardano/ed25519"
)

func pubFromPrvHex(prvKeyHex string) []byte {
	pb, _ := hex.DecodeString(prvKeyHex)
	return []byte(ed255192.ExtendedPrivateKey(pb[:64]).Public().(ed255192.PublicKey))
}

// demonstrates a correct binding: recompute address credentials from the
// signing public key and require them to match the address under test.
func addressBindsPubKey(pubKey []byte, addr Address) bool {
	payHash, _ := Blake224Hash(pubKey[:32])
	stakeHash, _ := Blake224Hash(pubKey[32:])
	return bytes.Equal(addr.Payment.Hash(), payHash) && bytes.Equal(addr.Stake.Hash(), stakeHash)
}

func TestPoC_FixedBinding(t *testing.T) {
	prvKeyB, err := DerivePrvKey(
		"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
		"m/1852'/1815'/0'/0/0",
	)
	if err != nil {
		t.Fatal(err)
	}
	pubB := pubFromPrvHex(prvKeyB)

	addressAStr := "addr1q8nrdx6sukqwatkv7x8y0csl0x2l0rek9cmc04n5z35anxphyemygs8dxvfe432u6xcrt89d968u478w6s0cu8x7thrsng2ztx"
	addrA, _ := NewAddress(addressAStr)

	if addressBindsPubKey(pubB, addrA) {
		t.Fatal("binding check failed to reject attacker key")
	}
	t.Log("FIXED check: attacker pubkey B does NOT match victim address A -> rejected")
}
