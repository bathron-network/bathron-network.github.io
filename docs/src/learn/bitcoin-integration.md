# Bitcoin integration

This is the load-bearing chapter. Everything BATHRON claims — no oracle, no federation, honest issuance — reduces to one capability: **the chain sees Bitcoin, inside consensus.**

## Headers

Bitcoin block headers are carried onto BATHRON in ordinary transactions and stored in an in-consensus header database. Every node independently validates each header's proof-of-work, difficulty adjustment and accumulated chainwork — exactly like a Bitcoin SPV client, except the client *is the consensus*. Reorgs on Bitcoin are followed by chainwork, like any Bitcoin node would.

## SPV

With the header chain in consensus, any Bitcoin transaction can be **proven** with a Merkle branch: the proof shows the transaction is included in a block buried under the accumulated work of the real Bitcoin chain. No one attests to this — every node checks it.

## Burn

The entry point for all value. Bitcoin is sent to a **provably unspendable** output, tagged with a destination on BATHRON. After enough confirmations, an SPV proof of the burn mints the same amount — one burned satoshi becomes one satoshi, with no issuer and no discretion. → [Monetary invariants](../reference/invariants.md)

## Proofs in scripts

The same machinery is exposed to **programs**. A covenant can require proof that a specific Bitcoin payment is confirmed — and release funds the moment it is:

```text
Alice pays on Bitcoin ──▶ proof lands on BATHRON ──▶ covenant releases
                         (Merkle proof, checked
                          by every node)
```

This is the primitive under the flagship use case: *a Bitcoin fact unlocks a contract*, verified by consensus, with no operator, oracle or custodian.

## Difficulty, time, chainwork

Scripts can also read Bitcoin's difficulty, timestamps and accumulated work from the in-consensus header chain. This is what makes an **oracle-free miner hedge** possible: the settlement condition is Bitcoin's own difficulty, not anyone's price feed. → [Miner hedging](applications/miner-hedging.md)

## What the link is — and is not

The link is **one-directional**. BATHRON can read Bitcoin facts and verify irreversible burns; it
cannot move native BTC or trigger a Bitcoin transaction. A return leg therefore requires a CP,
LP inventory and an explicit Bitcoin-side contract. Individual HTLC components have been tested,
but general atomicity is not claimed before the full state machine is specified and reviewed.
