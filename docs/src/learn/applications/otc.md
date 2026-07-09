# OTC settlement

Large trades have two enemies: **counterparty risk** and **information leakage**. OTC on BATHRON addresses both — settlement is atomic, and size is invisible.

```text
  quote agreed off-chain
          │
          ▼
  both legs locked (HTLC, same hash)
          │
          ▼
  atomic settlement ── amounts shielded
          │
          ▼
  no one saw the size; no one held the funds
```

## How it works

1. Two parties agree on a price off-chain — the protocol doesn't care how.
2. Each locks its leg under a hashlock keyed to the same secret; one leg can be native Bitcoin (proven by SPV or swapped atomically).
3. Settlement is atomic — both legs or neither — and the settlement-state side moves **shielded**: the market never learns the size.

## Why it matters

On a transparent chain, a large settlement is a public event that moves the market against you. Here, Bitcoin sees two unremarkable transactions; the trade itself is invisible.

**Primitives:** HTLC · shielded transfers · `TX_CONFIRMED` · atomic swaps
