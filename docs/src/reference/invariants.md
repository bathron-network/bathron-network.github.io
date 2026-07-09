# Monetary invariants

The money is protected by consensus rules, not by whoever signs blocks. Two invariants are checked at every block; a block that violates either is invalid everywhere, whatever signatures it carries.

## The internal units

Users send and hold satoshis; internally there are two forms:

```text
BTC ──(burn: irreversible, SPV-proven)──▶ M0            base unit
M0  ──(lock, 1:1, free)──▶ M1  ──(unlock, 1:1, free)──▶ M0    settlement receipt
```

`M0` is the base unit; `M1` is a receipt for vaulted `M0`, used by the settlement machinery. A user never touches either — they are implementation details of one thing: **satoshis backed by burned Bitcoin**.

## Invariant A5 — provenance

```text
M0_total == BTC provably burned
```

Every unit in existence corresponds to satoshis destroyed on Bitcoin, verified by SPV. No premine, no reward, no issuer — no exceptions, including genesis.

## Invariant A6 — parity

```text
M0_vaulted == M1_supply
```

Every receipt is backed by exactly one vaulted unit at all times. Lock and unlock are free and 1:1 in both directions, so no premium or discount can open: parity is enforced by arbitrage and checked by consensus.

## Why this matters

The finality quorum orders transactions; it has **no authority over the money**. A hypothetically malicious quorum could delay or reorder settlement — it could not mint a unit, break parity, or confirm an invalid transaction, because every node fully validates every block against these invariants. The supply is structurally beyond the reach of the signers.

A hard cap completes the picture: the supply can never exceed what Bitcoin's own schedule allows to be burned.
