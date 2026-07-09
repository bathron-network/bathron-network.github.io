# Examples

## The flagship, end to end

The canonical example is the flagship itself — **settle BTC for BTC, privately, with no custodian** — because it exercises every primitive in one flow. Both legs run on the live testnet today:

**Leg 1 — BTC in (trustless).** A real Bitcoin payment, proven by a Merkle branch against the in-consensus header chain, releases a covenant (`TX_CONFIRMED` gate) whose `CTV` template *forces* the payout to the user. The user then shields the funds — the private hop that breaks linkage — with the monetary invariants provably identical before and after.

**Leg 2 — BTC out (atomic).** A cross-chain atomic swap: one hashlock, two HTLCs — one on BATHRON, one on Bitcoin. Claiming either side reveals the preimage that settles the other; both legs were claimed live, and the preimage matched on both chains.

```text
BTC in ──▶ SPV proof ──▶ covenant releases ──▶ shield (private hop)
                                                  │
Bob gets BTC ◀── atomic HTLC swap ◀── settle with SP
```

Bitcoin saw two transactions. Everything between them was executed — and enforced — by the settlement state.

## Where the code lives

The node, tools and application code are published across the [BATHRON GitHub organization](https://github.com/bathron-network). Worked examples with the SDK — the patterns from [Applications](../learn/applications.md), runnable — ship with the public testnet.
