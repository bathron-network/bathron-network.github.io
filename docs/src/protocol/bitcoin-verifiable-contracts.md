# Bitcoin-verifiable contracts

A BATHRON script can assert a fact about the Bitcoin chain, and **every node checks it** against
headers the protocol already carries in consensus. No designated oracle takes part.

This is the primitive that distinguishes BATHRON. Everything on this page is `LIVE NOW` unless
marked otherwise.

## The five predicates

Defined in `src/script/btcstate.h`, evaluated by `OP_BTCSTATEVERIFY` in
`src/script/interpreter.cpp`:

| Query | Constant | Meaning |
|---|---|---|
| Difficulty at or above | `BTCSTATE_DIFF_GTE` | `difficulty(h) >= difficulty(nBits operand)` |
| Difficulty below | `BTCSTATE_DIFF_LT` | `difficulty(h) < difficulty(nBits operand)` |
| Height reached | `BTCSTATE_HEIGHT_GTE` | buried Bitcoin height `>= h` |
| Time passed | `BTCSTATE_MTP_GTE` | `median-time-past(h) >= operand` |
| Payment confirmed | `BTCSTATE_TX_CONFIRMED` | a Bitcoin transaction paying at least *amount* to a given `scriptPubKey`, included at height *h* with a Merkle proof, buried at least *minDepth* |

## The limits — read these before designing anything

**They are predicates, not readings.** A script asserts `difficulty(h) >= X`. It cannot *push* the
difficulty onto the stack. Binary and barrier payoffs are therefore native; a **linear** payoff must
be decomposed into steps, and each step costs script size.

**Only buried history is readable.** `BTCSTATE_REORG_MARGIN = 144` Bitcoin blocks — roughly a day.
Nothing more recent can be queried.

**Answers are snapshotted at the previous BATHRON block**, so a result never depends on transaction
order inside a block or on script-thread scheduling.

**Validity is monotone**, CLTV-style: a script that is not yet valid can become valid, never the
reverse.

**Fail-closed.** With no provider installed, every query evaluates false.

**No cumulative-work query exists**, and no *difficulty variation* predicate exists. A variation is
composed from two difficulty queries at two heights — that is possible, but it is composition, not
a primitive.

## What this makes possible without any oracle

- Hedges that settle on **mining difficulty itself**, at a threshold.
- Payments that open when a Bitcoin payment is **buried deep enough**.
- Time-bound agreements keyed to Bitcoin's own clock rather than a local one.
- Prediction instruments over **facts Bitcoin proves**.

## What it does not make possible

A price. An outside event. The state of another chain. None of these appears in a Bitcoin header,
and no combination of the five predicates produces one. Those need an external attestation —
see [Programmable settlement](programmable-settlement.md#external-attestations-dlc).

## Coverage note

`BTCSTATE_TX_CONFIRMED` is the most intricate of the five — Merkle proof, strict Bitcoin
serialization, and the 64-byte leaf ambiguity of CVE-2017-12842. It currently has **no dedicated
test suite**. Treat it as `AVAILABLE PRIMITIVE` with a known coverage gap rather than as a proven
path.
