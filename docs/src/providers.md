# Operate a provider

A useful quote needs inventory and an execution process behind it. A provider turns settlement primitives into a service by pricing an agreement, reserving the required assets, monitoring its legs and completing or recovering the operation under the agreed conditions.

Choose the role explicitly. A Settlement Provider handles BTC/M1 and carries an Operator identity, with block production optional. A Liquidity Provider handles X/M1; its Operator identity is optional.

## Working capital across pairs

Burning BTC creates M0, which can be locked one for one to create M1, the settlement unit a provider uses to quote pairs. One M1 inventory can be offered against any asset another provider quotes, giving it a common connection to all LPs through their quoted terms. For an Operator, the identity ticket burn is the entry capital for its identity: an irreversible cost, separate from inventory available for settlement. Existing M0 or M1 can also be acquired from holders.

## Define the service before quoting

Specify the asset pair, supported direction, sizes, fees, expiry and commitment point. Identify the external chain, evidence requirements and recovery process. Customers need to know when an offer binds the provider and when funds become committed.

Publish offers through direct connections, announcements, relays or indexers. An endpoint can be announced in ordinary on-chain data, but discovery and listing decisions remain outside consensus. An endpoint announcement identifies where to ask for service; it does not certify inventory or execution quality.

Inventory has several states: available, reserved for an accepted agreement, committed on-chain and eligible for recovery. Reconcile them separately. The same balance cannot support several firm obligations merely because they appear in different application records.

## Monitor every leg

Track transaction identifiers, relevant outputs, secrets, proofs and deadlines. Distinguish submission, inclusion and finality. For an external chain, apply its own observation rules and retain the data needed to resume after a service interruption.

A recovery branch needs an actor. Assign monitoring and submission to a defined process, with access to the required keys and transaction data. Follow the operation until its outputs are accounted for rather than stopping when the quote is accepted.

## Constrain professional inventory

Covenants can express approved destinations, staged withdrawals and recovery paths. A withdrawal can first enter a constrained staging output. A relative timelock makes the final destination spend eligible after a review period; a separately authorized recovery path provides an alternative under the encoded rules.

Recursive covenants can preserve the policy on successor inventory outputs. The builder must specify which branches remain eligible and which keys authorize them. A delay creates time for review; monitoring supplies the review itself.

These controls govern internal inventory. Shielded M0 transfers provide a separate way to move inventory before or after settlement.

## Publish evidence of the service

Make the link between an Operator identity and its provider role visible where applicable. Describe fees and observation policies in terms customers can compare. Publish verifiable service facts with a clear privacy scope. Users and applications interpret those facts; consensus supplies no reputation ranking.

Evaluate the business on actual costs: inventory, network transaction fees, external execution, monitoring and the option embedded in a quote's expiry. Provider charges and network fees are separate costs. See [How markets emerge](markets.md) and [Private inventory transfers](confidentiality.md) for discovery and disclosure choices.
