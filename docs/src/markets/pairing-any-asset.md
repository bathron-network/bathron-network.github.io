# Pairing an external asset against M1

The question a market builder asks first: *can I pair my asset?* The honest answer has two parts
— what the primitives make possible for any chain, and what has actually been demonstrated. This
page keeps them apart.

## The mechanism is chain-agnostic

Native BTC ⇄ M1 is paired with two hashlocked, timelocked contracts — one on each chain — keyed
to the same secret (→ [Native BTC ⇄ M1](native-btc-pair.md)). Nothing in that pattern is
specific to Bitcoin. It needs, on the other chain, exactly two things:

1. a **hashlock** — a script that pays only when a preimage is revealed;
2. a **timelock** — a refund path after a deadline (`CLTV`/`CSV` or equivalent).

Chains descended from Bitcoin's script (PIVX, DASH, Litecoin, Dogecoin, and many others) have
both. So do most chains with a scripting layer. **A chain that supports hashlocks and timelocks
can be paired against M1 the same way — one HTLC there, one HTLC here, same preimage.** No fork
of the other chain, no permission from its developers, no bridge, no wrapped asset.

```text
     other chain                             BATHRON
  ┌────────────────┐                    ┌────────────────┐
  │ HTLC(H) + CLTV │◄── same secret ───►│ HTLC(H) + CSV  │
  └────────────────┘                    └────────────────┘
       X inventory                          M1 inventory
                       X / M1  — a market, if someone quotes it
```

Chains without a scripting layer (or with only signature-based scripts) need adaptor-signature
constructions instead; that is a different piece of engineering and is not covered here.

## What is demonstrated, and what is not

| | Status |
|---|---|
| M1 HTLC on BATHRON + P2WSH HTLC on a Bitcoin test network, same preimage, both legs claimed | **demonstrated on testnet** |
| A general, atomic client service for BTC ⇄ M1 | not claimed — see [Status & claims](../consensus/status-and-claims.md) |
| Any pair other than BTC/M1 (PIVX, DOGE, LTC, …) | **capability of the primitives — nothing shipped, nothing tested** |
| Adaptor-signature pairing for script-less chains | not built |

You will not read on this site that BATHRON "supports" a given coin. It supports hashlocks and
timelocks; the market decides which coins get paired.

## Why pair against M1 rather than against BTC directly

Because of the hub (→ [The settlement unit](../provides/settlement-unit-m1.md)): with M1 as the
common leg, a provider holds one inventory and quotes many pairs, and every pair inherits the
depth of BTC/M1 instead of needing its own. And because M1 is what BATHRON's covenants can lock,
release, hedge and net — a DOGE/M1 market can be extended into DOGE-against-delivery, DOGE escrow
or a DOGE-denominated hedge without leaving the settlement layer.

## What it costs a market builder

Inventory in the paired asset, inventory in M1, a node on each chain, and the willingness to
quote first. That is the whole entry ticket. The delisting committee does not exist.

**Next:** [Settlement patterns](patterns.md)
