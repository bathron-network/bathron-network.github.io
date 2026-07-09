# Escrow

Escrow without an escrow agent: the funds are locked under a covenant, and **the release condition is a fact, not a decision**.

```text
  Buyer locks funds ──▶ covenant coffer
                            │
        condition met?      │        timeout?
   (proven Bitcoin payment, │   (CSV timelock)
    oracle signature, ...)  │
            │               │            │
            ▼               │            ▼
     pays the seller ◀──────┴──────▶ refunds the buyer
```

## How it works

1. The buyer locks funds under a script with two paths.
2. **Release path** — proof that the agreed condition happened: a specific Bitcoin payment confirmed (`TX_CONFIRMED`), or a designated third party's signature over an agreed message (`CSFS`). A covenant template (`CTV`) *forces* the payout to the seller — the buyer cannot redirect it.
3. **Refund path** — a relative timelock (`CSV`) returns the funds if the condition never occurs.

No agent holds the money. The "escrow service" is a script that every node enforces.

**Primitives:** `TX_CONFIRMED` · `CTV` · `CSV` · `CSFS`
