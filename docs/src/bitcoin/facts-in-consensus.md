# Bitcoin facts inside consensus

Markets that involve Bitcoin need to know things about Bitcoin: that a payment confirmed, that a
burn happened, what the difficulty is. The usual answer is an oracle — a party you trust to
report those things. BATHRON removes that party for one class of facts by carrying the Bitcoin
header chain inside its own consensus, so that every node checks the fact itself. This page
explains what that removes and what it still relies on.

## Headers and SPV proofs

Bitcoin block headers enter BATHRON in ordinary transactions. Every node checks each header the
way a Bitcoin light client would: proof of work, the difficulty adjustment schedule, timestamps
and accumulated chainwork. Reorganisations are followed by chainwork within pinned safety rules
— canonical checkpoints on the real chain and a floor below which no reorg is accepted.

Once the headers are there, a Merkle branch can prove that a specific Bitcoin transaction was
included under sufficient work. Every validating node evaluates the proof; no designated
operator attests to the event.

The Bitcoin chain read by consensus today is **Bitcoin testnet4**; mainnet will read Bitcoin
mainnet. The header database, reorg rules and burial requirements are documented in the
[SPV reference](../reference/spv.md).

## Conditional Bitcoin facts

A script can require proof that a specific Bitcoin payment is confirmed before releasing an
internal covenant:

```text
Bitcoin payment -> Merkle proof checked by consensus -> internal covenant may release
```

`TX_CONFIRMED` performs this check. It proves one component of a conditional settlement — the
"did the Bitcoin leg happen?" question — not a complete client service. What happens on the
Bitcoin side, the timeouts and the reorganisation behaviour of a full flow are specified by
whoever builds the market ([Native BTC ⇄ M1](../markets/native-btc-pair.md)).

## Difficulty, time and chainwork

Scripts can also inspect Bitcoin difficulty, timestamps and accumulated work. A
difficulty-linked contract therefore does not need a separate signer to report difficulty. A
complete hashprice contract still needs an external BTC price input — that fact is not on the
Bitcoin chain, so consensus cannot verify it ([Hedging on Bitcoin facts](../markets/patterns/hedging.md)).

The opcode-level detail — `OP_BTCSTATEVERIFY`, which fields are exposed, burial requirements —
lives in the [SPV reference](../reference/spv.md) and [Script & opcodes](../reference/opcodes.md).

## What this removes — and what it still depends on

**Removed:** a designated external oracle for Bitcoin facts. Nobody signs "the payment
confirmed"; every node computes it from headers and a Merkle branch.

**Still depended on:**

- **honest-majority Bitcoin hashpower** — the header chain BATHRON follows is the heaviest
  valid one it has seen; if Bitcoin itself were overpowered, so would be the facts read from it;
- **operator finality** — which BATHRON block a fact lands in is settled by
  [production and finality](../consensus/production-and-finality.md);
- **correct software** — the header validation and proof checking are code, and code can have
  bugs.

The scope is also fixed: BATHRON can *verify* Bitcoin facts and irreversible destructions; it
cannot move native BTC or trigger a Bitcoin transaction. Anything that must happen on Bitcoin
is done by a participant, on Bitcoin, with an explicit Bitcoin-side contract.

**Primitives:** `TX_BTC_HEADERS` · `TX_CONFIRMED` / `OP_BTCSTATEVERIFY` · `TX_BURN_CLAIM`
**See also:** [From destroyed BTC to M1](from-btc-to-m1.md) · [Status & claims](../consensus/status-and-claims.md)
