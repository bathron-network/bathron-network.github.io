# The infrastructure: what you can build on

The consensus settles; everything a market needs beyond that — conditions, delivery, timeouts,
privacy, pairing with other chains — is built from a small set of primitives that every node
enforces. This page is the builder's map: what the pieces are, and what each one lets a market
do. The opcode-level detail lives in the [reference](../reference/opcodes.md).

## Three layers, one boundary

```text
 ┌──────────────────────────────────────────────────────────────────┐
 │  MARKETS  (yours)                                                 │
 │  quotes · relays · order flow · providers · reputation · wallets  │
 ├──────────────────────────────────────────────────────────────────┤  ◄── consensus stops here
 │  BATHRON CONSENSUS                                                │
 │  M1 accounting · Bitcoin facts · covenants · finality             │
 ├──────────────────────────────────────────────────────────────────┤
 │  BITCOIN  (final asset)                                           │
 │  value · one-way origin of M0 · headers read by consensus         │
 └──────────────────────────────────────────────────────────────────┘
```

Everything above the line is permissionless by construction: the consensus never sees it, so it
cannot gate it.

## The primitives, by what they let a market do

| You want a market to… | Primitive | Where it is used |
|---|---|---|
| move native BTC in and out without a custodian | **hashlocks + timelocks** (HTLC family, `CSV`/`CLTV`) on both chains | [Native BTC ⇄ M1](../markets/native-btc-pair.md) |
| pair another chain that has hashlocks and timelocks | the same HTLC pattern, one leg per chain, **plus per-chain application work** | [Pairing an external asset](../markets/pairing-any-asset.md) |
| release one leg only when the other is proven | **`TX_CONFIRMED`** — a Bitcoin payment's Merkle proof checked against the in-consensus header chain | [DvP & OTC](../markets/patterns/dvp-otc.md), [Escrow](../markets/patterns/escrow.md) |
| force where funds go next | **`CTV`** (`OP_TEMPLATEVERIFY`) — commit to the spending transaction's template | escrow, provider controls |
| carry state across settlements (a contract that re-creates itself) | **output introspection** (`OP_OUTPUTVALUE`, `OP_OUTPUTSCRIPT`) — recursive covenants | rolling positions, standing rules |
| settle on an external fact (a price, a rate) | **`CSFS`** (`OP_CHECKSIGFROMSTACK`) — verify an oracle's signature in script | [Hedging](../markets/patterns/hedging.md), [Fixed-term value](../markets/patterns/fixed-term-value.md) |
| settle on a Bitcoin fact without any oracle | **`OP_BTCSTATEVERIFY`** — difficulty, height, median time read from consensus | [Hedging on Bitcoin facts](../markets/patterns/hedging.md) |
| keep size and counterparties private | **shielded transfers** (Sapling) on the internal leg | [Confidential settlement](../markets/confidential-settlement.md) |
| glue structured commitments | **`OP_CAT`** | inside the above |

Every settlement pattern in part III is a composition of this table — nothing else. If a use case
cannot be expressed here, the answer is a better composition, not a new opcode: the surface is
frozen (→ [Why the consensus is frozen](../consensus/why-frozen.md)).

## The shape of every application

1. **Lock value under a script** whose spending conditions you wrote.
2. **State the release conditions** — signatures, preimages, timeouts, a forced destination, an
   oracle signature, or a proven Bitcoin fact.
3. **Anyone can trigger settlement** once conditions are met. No server, no operator, no
   permission.

That is the whole developer model — a covenant, not a smart contract in the EVM sense.
→ [Build your first application](../operate/first-application.md)

## What is deliberately absent

No general-purpose VM, no gas market, no unbounded loops: scripts terminate, costs are predictable,
the validation surface stays auditable. No Taproot/Schnorr: ECDSA on secp256k1 throughout.

**Next:** [What BATHRON deliberately does not do](what-it-does-not-do.md)
