# BATHRON in five minutes

A contract needs more than a promise. It needs conditions that participants can inspect and rules that every validating node applies in the same way. BATHRON is an open programmable settlement protocol. It lets independent builders turn those conditions into payments, instruments and markets.

BATHRON provides settlement; providers operate the edges; third parties build the applications. Markets are one application of this layer.

## Bitcoin facts become contract conditions

Bitcoin already proves things. Now a contract can use them. BATHRON verifies Bitcoin headers and transaction proofs so a script can require a difficulty threshold, a reached height, a median time or a confirmed payment. Operators relay Bitcoin headers, with several sharing that interest and no designated relay. Each node verifies the evidence, including proof of work; a relay cannot invent a Bitcoin fact.

A price or a delivery in the physical world is different. An application can use a signed external attestation, with its source named in the agreement. See [Bitcoin facts in contracts](bitcoin-facts.md).

## Conditions compose

A covenant constrains where value goes next. A hashlock requires a secret. A timelock controls when a spending path opens. A signature authorizes an action or authenticates a statement. These primitives compose, including rules that carry forward into a successor output.

For example, an agreement can release a payment to a fixed recipient after a Bitcoin payment is proven, with a separate recovery path after an agreed deadline. The builder defines the complete agreement, including who submits each transaction. [Composable settlement](composition.md) explains the pieces.

## One settlement pivot

M0 is the base unit issued from verified Bitcoin destruction. M1 is its one-for-one vaulted receipt: the settlement unit handled by contracts and providers. Unlocking M1 releases M0.

Burning BTC creates M0, which can be locked one for one to create M1, the settlement unit a provider uses to quote pairs. One M1 inventory can be offered against any asset another provider quotes, giving it a common connection to all LPs through their quoted terms. For an Operator, the identity ticket burn is the entry capital for its identity: an irreversible cost, separate from inventory available for settlement.

End users settle in the assets they already hold; market builders and providers settle in M1. Providers connect this internal unit to external assets through markets. [M1: the settlement pivot](m1.md) separates the accounting rules from market prices.

## Confidential inventory transfers

Shielded M0 transfers can move inventory before or after settlement while keeping protected amounts private. [Private inventory transfers](confidentiality.md) explains the information exposed at each step.

## Discovery outside consensus

Providers publish offers through announcements, relays, indexers or direct connections. Discovery helps users find terms; it supplies neither inventory nor protocol approval. Users and applications interpret published service facts. See [How markets emerge](markets.md).

## Independent roles, shared rules

An Operator is a registered identity based on a burned ticket and maturity; one Operator, one vote; it may produce blocks and sign finality. Settlement Providers handle BTC/M1 and carry an Operator identity, whether or not they produce blocks. Liquidity Providers handle X/M1, with an optional Operator identity. Builders create applications; users choose their agreements; observers verify independently.

Consensus checks settlement conditions. Providers supply quotes, inventory and execution services. Objectively proven double signing permanently bans the Operator identity; there is no slashing.

Start with [Where trust lives](trust.md) to understand these responsibilities, or explore [What you can build](applications.md) for concrete examples. A primitive alone does not supply an application: an application also needs terms, software, operators of its services and a reason for people to use it.
