# SPV verification

How BATHRON sees Bitcoin without an oracle — the machinery behind [Bitcoin integration](../learn/bitcoin-integration.md).

## The header database

Bitcoin headers enter via `TX_BTC_HEADERS` transactions and live in a consensus-maintained database. Every node validates, per header: proof-of-work against the encoded target, the difficulty adjustment schedule, timestamp rules, and accumulated **chainwork**. Anyone can submit headers; invalid ones are consensus-rejected.

## Following the real chain

- **Reorgs are handled by chainwork**, like a Bitcoin node: a heavier branch replaces a lighter one, with full undo support.
- **Canonical checkpoints**: headers at fixed anchor heights must match pinned hashes of the real Bitcoin chain — a from-scratch fake chain, even a well-formed one, cannot be grafted in.
- **A reorg floor**: no reorg is accepted below a pinned checkpoint or below a burn that has already minted — an accepted burn cannot be un-happened.

## Proving a transaction

A Bitcoin transaction is proven with a **Merkle branch** to a block header in the database, plus a burial requirement (confirmations of chainwork on top). Verification is pure computation — hash the branch, compare the root, check the depth — performed by every node.

## Two consumers

| Consumer | Use |
|---|---|
| **Burn claims** (`TX_BURN_CLAIM`) | prove a Bitcoin burn, mint 1:1 after maturity |
| **Scripts** (`TX_CONFIRMED` via `OP_BTCSTATEVERIFY`) | any covenant can require proof of a Bitcoin payment |

The same rules serve both — there is no privileged path and no bypass, including at genesis: the very first mint was SPV-verified like every one since.

## Burn format (BCS v1.0)

A Bitcoin burn that BATHRON can mint from is a standard Bitcoin transaction with two required outputs:

```text
OP_RETURN   BATHRON|01|<NET>|<DEST_HASH160>   (29 bytes: "BATHRON" magic + version + network + P2PKH dest hash160)
value out   P2WSH(OP_FALSE)                    (provably unspendable — the BTC is destroyed)
```

`P2WSH(OP_FALSE)` commits to `SHA256(0x00) = 6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d`; the script can never be satisfied, so the coins are gone. The `OP_RETURN` names the BATHRON destination that receives the minted M0. A burn is unique by `(btc_txid, vout)`; duplicates are rejected.

## Maturity and genesis constants

| Constant | Testnet | Mainnet | Meaning |
|---|---|---|---|
| `K_BTC_CONFS` | 6 | 24 | Bitcoin confirmations required before a burn is claimable |
| `K_FINALITY` | 20 | 100 | BATHRON blocks after the claim before the mint is eligible |

Genesis is the same path, not a special case: block 0 is an empty coinbase, block 1 is the first `TX_MINT_M0BTC` (SPV-verified exactly like every later mint), and operator registrations follow. No burn is ever hardcoded — every minted satoshi traces to a verified Bitcoin destruction.
