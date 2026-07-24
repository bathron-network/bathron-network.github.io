# Transaction types

Beyond standard transactions, the settlement state is maintained by a small set of special transaction types, each with its own consensus validation.

| Type | ID | Purpose |
|---|---|---|
| `NORMAL` | 0 | standard payment — transparent or shielded (Sapling) |
| `PROREG` | 1 | register an operator identity using locked M0 collateral (M0 the operator may have acquired from a third party) |
| `TX_LOCK` | 20 | vault M0, issue a 1:1 M1 receipt |
| `TX_UNLOCK` | 21 | redeem a receipt, release the vaulted M0 |
| `TX_TRANSFER_M1` | 22 | transfer a receipt between parties |
| `TX_BURN_CLAIM` | 31 | submit the SPV proof of a Bitcoin burn |
| `TX_MINT_M0BTC` | 32 | mint M0 against a matured, verified burn claim |
| `TX_BTC_HEADERS` | 33 | carry Bitcoin block headers into consensus |

An **HTLC family** of settlement transactions (create / claim / refund, hashlock + timelock) powers atomic swaps and the DvP patterns.

## Design notes

- **Special transactions cannot carry shielded components.** Privacy lives in `NORMAL` transactions only; the settlement skeleton stays fully auditable — this is consensus-enforced, not convention.
- **Receipts are protected at consensus level.** An M1 receipt output can only be spent by the settlement types that understand it (`TX_UNLOCK`, `TX_TRANSFER_M1`, HTLC) — never accidentally swept by a normal payment.
- **Fees are strict.** The coinbase must equal the block's fees exactly — a producer can neither inflate nor quietly divert.
