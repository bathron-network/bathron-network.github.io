# Delivery-versus-payment and OTC

The settlement problem in one line: **neither side should be able to take delivery without
paying, or pay without taking delivery.** Traditional finance solves it with a clearing house
that holds both legs. A market on BATHRON solves it with a covenant: both legs are locked under
the same condition, and they settle together or refund together. OTC settlement is the same
pattern with one addition — the size of the trade stays hidden.

## Delivery versus payment

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

Both legs are locked under scripts keyed to the **same hash**. Claiming one leg requires
revealing the preimage — which is exactly what the counterparty needs to claim the other.
Timeouts (`CSV`/`CLTV`) guarantee that an abandoned trade refunds both sides.

The legs do not need to live on the same chain: one can be a native Bitcoin transaction,
either proven by SPV (`TX_CONFIRMED`) or paired as an HTLC keyed to the same hash. That is how
the [native BTC ⇄ M1 pair](../native-btc-pair.md) works — DvP where one deliverable is
bitcoin.

Atomic settlement needs programmability (which Bitcoin refuses) plus verification of Bitcoin
facts (which nobody else has without an external attester). The combination is the niche.

## OTC: DvP with shielded size

Large trades have two enemies: counterparty risk and information leakage. The paired legs
address the first; shielded transfers address the second.

```text
  quote agreed off-chain
          │
          ▼
  both legs locked (HTLC, same hash)
          │
          ▼
  both-or-neither settlement ── amounts shielded
          │
          ▼
  no one saw the size; no one held the funds
```

1. Two parties agree on a price off-chain — the protocol does not care how.
2. Each locks its leg under a hashlock keyed to the same secret; one leg can be native Bitcoin.
3. The paired legs settle both-or-neither, and the M1 side moves **shielded**: the market
   never learns the size.

On a transparent chain, a large settlement is a public event that moves the market against
you. Here, Bitcoin sees two unremarkable transactions; the trade itself is invisible.

These pages describe component-level behaviour; see
[Status & claims](../../consensus/status-and-claims.md).

**Primitives:** hashlocks (HTLC) · `CSV` / `CLTV` · `TX_CONFIRMED` · shielded transfers

**See also:** [Confidential settlement](../confidential-settlement.md)
