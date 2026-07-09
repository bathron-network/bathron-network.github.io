# Delivery versus payment

The settlement problem in one line: **neither side should be able to take delivery without paying, or pay without taking delivery.** Traditional finance solves it with a clearing house. A covenant solves it with atomicity.

```text
  Leg A: payment                Leg B: delivery
        │                             │
        └────── one shared secret ────┘
                       │
        claiming either leg reveals it —
        the other leg becomes claimable
                       │
        both settle, or both refund
```

## How it works

Both legs are locked under scripts keyed to the **same hash**. Claiming one leg requires revealing the preimage — which is exactly what the counterparty needs to claim the other. Timeouts (`CSV`) guarantee that an abandoned trade refunds both sides.

The legs don't need to live on the same chain: one can be a native **Bitcoin** transaction, proven by SPV or settled as a cross-chain atomic swap. That is how the flagship BTC↔BTC settlement works — DvP where both deliverables are bitcoin.

## Why here

Atomic settlement needs programmability (Bitcoin refuses it) plus Bitcoin-fact verification (nobody else has it without an oracle). The combination is the niche.

**Primitives:** hashlocks (HTLC) · `CSV` · `TX_CONFIRMED` · atomic swaps
