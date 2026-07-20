# Accounting invariants

Two consensus rules constrain the internal units. They establish provenance and conservation;
they do not establish an external market price or a redemption promise.

## Internal units

```text
BTC --irreversible, SPV-proven destruction--> M0
M0 ----------------lock 1:1-----------------> M1
M1 ----------------unlock 1:1---------------> M0
```

M0 is the base accounting unit. M1 is created when M0 is vaulted and is used as programmable
settlement state by CPs and LPs in the target architecture.

## A5 — provenance

```text
M0_total == BTC provably destroyed
```

Every M0 unit originates from a verified destruction. There is no premine, block reward, issuer or
genesis exception. Because the BTC is destroyed rather than reserved, M0 is not redeemable for it.

## A6 — internal accounting equality

```text
M0_vaulted == M1_supply
```

Lock and unlock are protocol operations at 1:1. This prevents creation of unvaulted M1. It does
not prevent a market discount: external liquidity for M1 can be absent and its realizable value
can be zero.

## Security consequence

A finality quorum orders transactions but cannot create M0 without a valid burn claim or create M1
without vaulted M0. This limits consensus authority over supply; it does not remove application,
liquidity, software or legal risk.
