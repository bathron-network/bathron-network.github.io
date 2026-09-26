# What consensus enforces

Participants need a common answer to whether a settlement follows its rules. They do not need consensus to choose a business model or decide which market deserves customers. BATHRON separates those responsibilities: validation checks the agreement encoded in transactions, while commercial decisions remain with applications and their users.

## The rules every node checks

Nodes verify that inputs are spendable, authorization is valid and script conditions hold. They check Bitcoin evidence against the accepted header view. They enforce monetary provenance and conservation, including the relationship between vaulted M0 and M1 receipts.

A transaction must satisfy those rules regardless of who submits it or which provider arranged it. A signature used for finality does not grant permission to skip transaction validation.

| Consensus knows | Consensus does not know |
|---|---|
| Whether conservation rules hold | The market value of a balance |
| Whether a Bitcoin predicate is satisfied | An exchange rate reported by a business |
| Whether spending conditions hold | Whether the agreement is commercially attractive |
| Which identities sign consensus messages | Which provider a customer should prefer |
| Whether a transaction follows fee rules | Which pairs deserve liquidity |

Here, “knows” means verifies the relevant evidence. It does not mean that every confidential amount or balance is publicly readable.

## Finality sits above validation

Validation answers whether a state transition is permitted. Finality establishes agreement on validated history. These functions work together, in that order. Operators cannot turn an invalid monetary operation into a valid one by signing it.

An application distinguishes a submitted transaction, inclusion in a block and finality. It also tracks any external leg separately. A final BATHRON payment is evidence about BATHRON settlement, not a command to another chain.

## Why these boundaries matter

BATHRON has no listing committee, protocol order book or preferred market maker. A provider quotes a price; a user accepts terms; a transaction expresses the resulting settlement conditions. Consensus checks those conditions without adopting the quote as an official price.

Similarly, verifying an oracle signature authenticates a statement from the agreed source. It does not make consensus an arbitrator of the underlying event. [Where trust lives](trust.md) explains how to identify that dependency.

The boundary preserves room for competing applications. Builders can change discovery, interfaces, pricing and service policies without asking every node to adopt those choices. Applications using existing primitives do not need new consensus rules.

These guarantees have a defined scope: provenance, conservation, valid conditions and agreement on history. [Where trust lives](trust.md) sets out their economic and cross-chain limits. See [Network operators](operators.md) for consensus responsibilities and [Monetary invariants](invariants.md) for accounting details.
