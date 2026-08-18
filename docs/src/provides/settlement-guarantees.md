# Settlement guarantees: what consensus enforces

A market built on BATHRON relies on one thing from the protocol: that a settlement, once final,
happened exactly as its rules said and can never be undone or forged. This page lists what the
consensus guarantees — and, just as importantly, what it deliberately does not know.

## What every node enforces

Every node fully validates every block; finality is added on top of that validation, never instead
of it. Four families of rules:

| Guarantee | What it means for your market |
|---|---|
| **Accounting integrity** | one destroyed satoshi permits one M0; vaulted M0 always equals the M1 supply; the coinbase equals the block's fees exactly. No unit can be created by anyone — not by a producer, not by a finality quorum. |
| **Bitcoin facts** | Bitcoin block headers are carried and checked inside consensus (proof of work, difficulty, chainwork). A Merkle proof can therefore establish, for every node, that a specific Bitcoin transaction is confirmed — no designated oracle. |
| **Contract conditions** | a covenant's spending rules — signatures, hashlocks, timelocks (`CSV`/`CLTV`), forced destinations (`CTV`), oracle signatures (`CSFS`), Bitcoin-fact checks (`TX_CONFIRMED`) — are evaluated identically by every node. When conditions are met, anyone can trigger the settlement; when they are not, nobody can. |
| **Transfers and finality** | M1 moves only through the settlement transaction types that understand it (lock, unlock, transfer, HTLC family) — never swept by accident. A block is final after one round of operator signatures, about a minute; once final it cannot be reorganised, whatever the chainwork. |

Confidential transfers keep amounts and linkage hidden while consensus still verifies conservation
(→ [Confidential settlement](../markets/confidential-settlement.md)).

## What consensus deliberately does not know

```text
   CONSENSUS KNOWS                          CONSENSUS DOES NOT KNOW
   ─────────────────                        ────────────────────────
   every balance and receipt                any price
   every verified Bitcoin fact              any order book or quote
   whether a contract's conditions hold     which pairs exist
   who signed finality (1 operator = 1 vote) who is a "good" provider
   the fees of a block                      whether a market is worth listing
```

This is not a gap to be filled later. Prices, quotes, order books, provider selection and
reputation are **market-layer** facts. Keeping them out of consensus is what makes the protocol
neutral: it cannot favour a pair, a provider or a price because it does not see them.
→ [What BATHRON deliberately does not do](what-it-does-not-do.md)

## What a captured finality threshold could and could not do

The full analysis is on [Security model](../consensus/security-model.md); the short version:

- It **cannot** create a unit, break the M0↔M1 accounting, spend a client's key or force a
  Bitcoin transaction — full validation rejects all of that regardless of signatures.
- It **can** censor an operation, stall finality, or present divergent finalized views across a
  partition. Settlement is only reversible until it finalizes (~1 minute), so what is at risk is
  timing, never the money.

Operator admission is not yet open — the current operator set is project-run while the
open-admission threat model is worked. → [Status & claims](../consensus/status-and-claims.md)

**Next:** [The infrastructure: what you can build on](infrastructure.md)
