# Conditional payments and escrow

Two parties can agree on a payment before its release condition is satisfied. An escrow makes that separation explicit: value is committed under spending rules, then a permitted transaction releases or recovers it. BATHRON gives builders the primitives to encode those rules.

The first design question is what counts as completion. A Bitcoin payment can be proven cryptographically. Physical delivery or satisfactory work requires evidence from outside the protocol. The contract should make that difference visible to both parties.

## Write the agreement before the script

Suppose Alice commits a payment for Bob. Their agreement names the amount, recipient, release evidence and recovery condition. A covenant constrains the payment destination. Signatures express authorization. A Bitcoin predicate or an external attestation supplies the chosen evidence. A timelock controls eligibility for a timed path.

The lock, seal, eye and clock from [Composable settlement](composition.md) help explain this agreement without requiring the user to read opcodes.

| Stage | What the application establishes |
|---|---|
| Funding | The agreed value enters the output with the agreed conditions |
| Release | Required authorization and evidence permit the specified payment |
| Recovery | The recovery conditions permit a spend to the agreed destination |
| Completion | The application observes the resulting transaction and its finality |

## Define overlapping paths

A recovery deadline does not automatically disable every other branch. The builder specifies which paths remain valid and how the agreement treats a race between eligible spends. The user-facing explanation must match those actual conditions.

Likewise, “payment confirmed” must name the relevant Bitcoin output script, amount and required evidence. “Delivered” must name the source authorized to attest delivery. Vague commercial language cannot replace an exact spending condition.

## Assign monitoring

A refund right is useful only if Alice's software watches the chain and acts when needed. The agreement names the monitoring responsibility, the data required to recover and the keys that authorize the spend. Applications retain enough information to resume this work after an interruption.

For a human dispute, parties can choose an arbitrator and encode the resulting authorization path. BATHRON checks the required signature. The arbitrator's judgment remains an external part of the agreement.

An escrow is therefore a complete workflow, not just a locked output. [Build an application](build.md) explains how to review each transition. [Contracts on Bitcoin facts](bitcoin-contracts.md) develops examples where the release evidence comes directly from Bitcoin history.
