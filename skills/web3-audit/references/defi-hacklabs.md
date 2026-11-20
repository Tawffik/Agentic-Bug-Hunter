# DeFiHackLabs — runnable exploit precedent

DeFiHackLabs (https://github.com/SunWeb3Sec/DeFiHackLabs) contains 900+ real
DeFi incidents reproduced as Foundry tests. Use it to learn the **shape** of an
exploit, then prove the same missing check exists in the in-scope code.

## Local search

```bash
git clone --depth 1 https://github.com/SunWeb3Sec/DeFiHackLabs ~/.cache/defi-hacklabs
DEFI_HACKLABS_DIR=~/.cache/defi-hacklabs bash bughunter/tools/defi_hack_search.sh oracle
DEFI_HACKLABS_DIR=~/.cache/defi-hacklabs bash bughunter/tools/defi_hack_search.sh flashloan --limit 40
DEFI_HACKLABS_DIR=~/.cache/defi-hacklabs bash bughunter/tools/defi_hack_search.sh "multicall" --all
```

The tool searches `src/`, `past/`, `academy/`, and the README. A hit is a
**LEAD**; the PoC is precedent from a different deployment, not evidence about
the target.

## Query map

| Hunt question | Search terms |
|---|---|
| Accounting desync / phantom value | `totalSupply`, `totalAssets`, `exchangeRate`, `rewardPerShare`, `accounting` |
| First-depositor / share inflation | `inflation`, `donation`, `first deposit`, `previewDeposit`, `convertToShares` |
| Reentrancy / read-only reentrancy | `reentrancy`, `callback`, `onERC721Received`, `getReserves`, `view` |
| Oracle / flash-loan manipulation | `oracle`, `flashloan`, `TWAP`, `getPrice`, `manipulate` |
| Access control / missing modifier | `onlyOwner`, `initialize`, `proxy`, `admin`, `role` |
| Signature replay / permit | `permit`, `ecrecover`, `signature`, `nonce`, `chainId` |
| Bridge / cross-chain | `bridge`, `message`, `root`, `validator`, `finalize` |
| AMM / LP math | `swap`, `reserve`, `k`, `liquidity`, `skim`, `sync` |
| Lending / liquidation | `liquidate`, `collateral`, `borrow`, `health`, `badDebt` |
| Token quirks | `feeOnTransfer`, `rebasing`, `decimals`, `balanceOf`, `transferFrom` |
| Payable multicall / msg.value reuse | `multicall`, `msg.value`, `delegatecall`, `aggregate` |
| Upgrade / storage collision | `upgradeTo`, `implementation`, `slot`, `initialize`, `UUPS` |

## How to use a match

1. Read the PoC's `setUp()` — which fork block, contracts, and actors?
2. Read the exploit body — which call sequence and state transition causes loss?
3. Extract the **precondition** (missing check, stale value, wrong ordering).
4. Search the target for that precondition; if absent, kill the lead.
5. If present, copy the PoC's *shape* (not its addresses) into a target-local
   Foundry test on a pinned fork block.

Do not submit a past exploit as a finding. Cite it only as precedent after the
target-local PoC passes.
