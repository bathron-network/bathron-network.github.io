# OTC settlement

Large trades have two enemies: **counterparty risk** and **information leakage**. OTC on BATHRON addresses both — the paired legs are designed to settle both-or-neither, and size is invisible.

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

## How it works

1. Two parties agree on a price off-chain — the protocol doesn't care how.
2. Each locks its leg under a hashlock keyed to the same secret; one leg can be native Bitcoin (proven by SPV or swapped atomically).
3. The paired HTLC legs settle both-or-neither, and the settlement-state side moves **shielded**: the market never learns the size.

## Why it matters

On a transparent chain, a large settlement is a public event that moves the market against you. Here, Bitcoin sees two unremarkable transactions; the trade itself is invisible.

As with every pattern on these pages, this describes component-level behaviour;
a generally atomic client service is not claimed yet (see the
[FAQ](../../faq.md)).

**Primitives:** HTLC · shielded transfers · `TX_CONFIRMED` · atomic swaps
