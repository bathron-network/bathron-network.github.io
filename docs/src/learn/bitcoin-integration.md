# Bitcoin integration

This is the load-bearing technical chapter. BATHRON carries and validates Bitcoin headers inside
its own consensus. That removes a designated external attestation oracle for Bitcoin facts, but
it still depends on honest-majority Bitcoin hashpower, BATHRON operator finality and correct
software.

## Headers and SPV proofs

Bitcoin headers enter in ordinary BATHRON transactions. Every node checks proof of work,
difficulty adjustment, timestamps and accumulated chainwork. Bitcoin reorganisation handling
follows chainwork within the pinned safety rules documented in the [SPV reference](../reference/spv.md).

A Merkle branch can then prove that a Bitcoin transaction was included under sufficient work.
Every validating node evaluates the proof; no designated operator attests to the event.

## Conditional Bitcoin facts

A program can require proof that a specific Bitcoin payment is confirmed before releasing an
internal covenant:

```text
Bitcoin payment -> Merkle proof checked by consensus -> internal covenant may release
```

`TX_CONFIRMED`, built on `OP_BTCSTATEVERIFY`, performs this check. It proves one component of a
conditional settlement, not a complete client service. The external return leg, timeouts and
reorganisation behaviour must be specified separately.

## Professional inventory origin

M0 can originate only when Bitcoin is sent to a provably unspendable output and the destruction
is verified by consensus. This is an irreversible inventory-acquisition path for professional
providers, not the client product. The BTC is not held for redemption. → [Accounting
invariants](../reference/invariants.md)

## Difficulty, time and chainwork

Scripts can also inspect Bitcoin difficulty, timestamps and accumulated work. A difficulty-linked
contract therefore does not need a separate signer to report difficulty, under the SPV, operator
and software assumptions above. A complete hashprice contract still needs an external BTC price
input. → [Miner hedging](applications/miner-hedging.md)

## What the link is—and is not

BATHRON can verify Bitcoin facts and irreversible burns; it cannot move native BTC or trigger a
Bitcoin transaction. A return leg therefore requires a CP, LP inventory and an explicit
Bitcoin-side contract. Individual HTLC components have been tested, but general atomicity is not
claimed before the full state machine is specified and reviewed.
