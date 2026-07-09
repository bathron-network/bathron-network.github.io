# Architecture

The whole system is one vertical flow:

```text
        Bitcoin
           │
           ▼
         Burn
           │
           ▼
  Shared settlement state
           │
           ▼
      Applications
           │
           ▼
  Settlement Providers
           │
           ▼
     Native Bitcoin
```

## Bitcoin

The source of truth. BATHRON carries the Bitcoin header chain **inside its own consensus**: every node validates Bitcoin proof-of-work and chainwork, and scripts can verify Merkle proofs against it. No oracle reports Bitcoin facts — the chain checks them itself. → [Bitcoin integration](bitcoin-integration.md)

## Burn

The only way value enters. Bitcoin is sent to a provably unspendable output; after enough confirmations, an SPV proof of that burn mints the same amount on BATHRON, satoshi for satoshi. Irreversible, verifiable by everyone, with no issuer. → [Monetary invariants](../reference/invariants.md)

## Shared settlement state

The kernel itself: one state, maintained by consensus, that all applications read and write. Deterministic block production every 60 seconds, BFT finality in about a minute, shielded transfers for privacy. → [Consensus](consensus.md), [Privacy](privacy.md)

## Applications

Covenants written against the settlement state: payments, escrow, DvP, vaults, OTC. They are scripts enforced by every node — not services run by anyone. → [Applications](applications.md)

## Settlement Providers

The exit to native BTC. An open market of providers quotes prices and supplies Bitcoin liquidity, competing on fees. The protocol never custodies and never sells. → [Settlement Providers](settlement-providers.md)

## Native Bitcoin

Where users end up. Bitcoin sees two transactions — one in, one out. BATHRON executes everything in between.
