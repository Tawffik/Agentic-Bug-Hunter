# Web3 reentrancy lab (authorized, local)
Vulnerable `Bank` (CEI violation) + `Attacker` that re-enters and drains it.
Proves REENTRANCY-01 detection with a deterministic Foundry PoC.
```bash
cd tests/benchmark/web3_reentrancy && forge install foundry-rs/forge-std && forge test -vv
```
