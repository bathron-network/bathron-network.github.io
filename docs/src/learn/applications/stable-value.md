# Stable value

The discipline first: **BATHRON will never mint a stablecoin.** No global debt, no protocol-issued dollar, no peg to defend. What the primitives allow is different — and sounder: **stability as a position, between two consenting parties.**

```text
  party A (wants dollar stability)     party B (wants BTC exposure)
              │                                   │
              └────── both lock sats in a covenant ──────┘
                               │
                               ▼
              at expiry, a signed price (CSFS)
              splits the pot so that A receives
              the dollar value of A's deposit
```

## How it works

A discreet-log-contract-style covenant: two parties lock satoshis; at expiry, a published price signature determines the split. Party A gets dollar-stable value; party B gets leveraged BTC exposure. The "stablecoin" is a **contract outcome**, collateralized in full, expiring on schedule.

## Why not a minted dollar?

Minted stablecoins concentrate three risks the design refuses: an issuer (custody), a peg (bank-run dynamics), and a global liability (everyone depends on one balance sheet). A position has none — its risk is bilateral, priced, and expires.

## The honest caveat

The price is not an on-chain fact; the oracle signature (`CSFS`) is a real trust assumption, mitigated — not removed — by choosing and diversifying signers.

**Primitives:** covenants · `CSFS` · `CSV`/`CLTV` expiry · shielded balances
