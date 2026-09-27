# Glossary

These terms distinguish protocol rules from commercial services. A single organization can hold several roles, but the responsibilities remain separate. Follow the linked pages for the full workflows and evidence requirements.

## Units and settlement

**BATHRON:** An open programmable settlement protocol. It provides common validation rules, Bitcoin fact verification and programmable conditions for independent applications.

**M0:** The base accounting unit originating from verified, irreversible Bitcoin destruction. Ownership can change without changing that provenance.

**M1:** The settlement receipt created one for one by vaulting M0. Consuming it through unlock releases M0, not BTC. See [M1](m1.md).

**Burn:** Provable destruction of BTC used to establish monetary origin. It creates no recoverable Bitcoin reserve.

**Settlement pivot:** A common intermediate unit connecting asset pairs. The arrangement simplifies connections without supplying their inventory or prices.

**Settlement:** Completion of an agreed transfer through valid transactions. External legs require their own execution and observation. See [Settlement across chains](cross-chain.md).

**Validation:** Checking that a transaction or block satisfies the protocol rules, including authorization, evidence and conservation. See [What consensus enforces](boundaries.md).

**Finality:** Agreement on validated history. It sits above transaction validation and does not replace it.

## People and services

**Operator:** A registered identity admitted through a burned ticket and maturity. The entry cost is real, visible and permanently spent; one Operator, one vote; may produce blocks and sign finality.

**Settlement Provider (SP):** A BTC/M1 provider with an Operator identity. It handles inventory, quotes and external execution; it can produce blocks or operate without producing them.

**Liquidity Provider (LP):** An X/M1 provider managing liquidity and the external asset leg. Its Operator identity is optional.

**Builder:** Someone creating an application, agreement, interface or service using the infrastructure.

**User:** A participant choosing terms and authorizing an application's operations.

**Observer:** A participant independently verifying history or publishing evidence about network and service activity. See [Who does what](roles.md).

**Ban:** Permanent ban for objectively proven double signing; no slashing. The burned identity ticket remains spent. See [Network operators](operators.md).

**Pause:** An interruption in progress or finality.

**Quote:** A provider's offer with defined terms and expiry. It is separate from a funded settlement transaction.

## Conditions and evidence

**Covenant:** A script condition constraining the transaction that spends an output. A recursive covenant preserves a policy in successor outputs.

**Hashlock:** A condition requiring a secret whose hash matches the committed value.

**Timelock:** A time or height condition making a spending path eligible.

**HTLC:** A hashlocked, timelocked construction. Coordinating HTLCs across chains also requires chain-specific execution and monitoring.

**Bitcoin predicate:** A pass-or-fail condition about accepted Bitcoin history, such as difficulty, height, median time or a proven payment.

**SPV proof:** Transaction inclusion evidence checked against a verified header view, together with the applicable eligibility checks.

**Attestation:** A signed statement from an external source. Signature verification authenticates the source; it does not establish the truth of an outside event.

**DLC:** Discreet log contract: a construction connecting agreed outcomes to an external attestation and defined settlement paths.

**Recovery path:** An alternative spend with specified conditions, authorization and destination.

**Confidential transfer:** A shielded M0 transfer whose protected details are verified without being published. It can move inventory before or after settlement. See [Private inventory transfers](confidentiality.md) for its scope.

**USDBTC:** A possible third-party risk-transfer application; see [What you can build](applications.md#usdbtc).
