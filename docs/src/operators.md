# Network operators

A settlement network needs participants to validate transactions, produce blocks and establish agreement on history. BATHRON assigns these consensus responsibilities to Operators while preserving independent validation by nodes. Operating a commercial service is a separate role.

An Operator is a registered identity based on a burned ticket and maturity; one Operator, one vote; it may produce blocks and sign finality. A Settlement Provider carries this identity but can provide BTC/M1 service without producing blocks. The identity connects public participation to accountability; it is not an endorsement of a provider's commercial terms.

The ticket burn is a real, publicly visible and irreversible entry cost. Maturity adds an admission condition before the identity can participate. A permanent ban does not return the burned ticket.

## Consensus responsibilities

- **One Operator, one vote.** Consensus participation follows Operator identity, not a provider's trading volume or a customer's balance.
- **Permanent ban for objectively proven double signing; no slashing.** The ban removes the offending identity's eligibility. The admission cost has already been spent through the ticket burn.
- **Finality above validation.** Agreement on history applies to validated blocks. Signatures do not override monetary or script rules.

Transactions follow the same validity rules whoever submits them.

## Three distinct functions

Validation checks whether a transaction and the resulting state obey the protocol. Block production proposes an ordered collection of transactions. Finality establishes agreement on validated history. Applications track these functions separately instead of treating a submitted transaction as completed settlement.

Each validating node checks the rules itself. An Operator cannot make an unauthorized spend valid, mint M0 without valid provenance or create M1 without the corresponding vaulted M0 by adding a signature.

## Keep identities and duties clear

An operator of infrastructure protects signing keys, maintains records and monitors its node. It distinguishes consensus signing from wallet authorization and commercial service credentials. Publicly associating a provider with an Operator identity makes the combined roles visible to users and observers.

Double-signing accountability concerns objectively verifiable conflicting consensus signatures. A customer's complaint about a quote is a commercial matter, not that proof. The distinction keeps protocol sanctions separate from a marketplace reputation system.

## Observe without operating

Running a validating node does not require selling liquidity or producing blocks. Observers can inspect transactions, accounting and finality independently. The network's rules are shared; the services built around them remain independently operated.

See [What consensus enforces](boundaries.md) for the validation boundary, [Who does what](roles.md) for provider identities, and [Run and observe a node](node.md) for independent verification.
