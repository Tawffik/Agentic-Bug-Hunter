# Web3 access-control lab (authorized, local)

A deliberately vulnerable `Vault` (unprotected `initialize`/`mint`/`setOwner`) plus a
SafeVault (guarded) — used to test `web3_evm_hazard_scan.py` ACCESS-CONTROL-01 and to
prove exploitability with a deterministic Foundry PoC.

```bash
cd tests/benchmark/web3_access_control
forge install foundry-rs/forge-std   # first run
forge test -vv                       # exploit tests PASS => vulnerability confirmed
```

The scanner unit test (`tests/test_web3_access_control.py`) needs no Foundry.
