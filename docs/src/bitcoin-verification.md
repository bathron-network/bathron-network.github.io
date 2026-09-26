# Bitcoin verification

BATHRON uses Bitcoin evidence for monetary origin and contract conditions. Nodes verify that evidence through an accepted header view and transaction proofs. The submitter brings data; the validating node decides whether the data satisfies the rules.

Operators have an interest in keeping Bitcoin evidence available, and several relay headers without a designated relay. Every node checks proof of work and the other header rules: a relay brings evidence, not authority to invent a Bitcoin fact. Keeping that evidence current still requires relaying and inclusion.

## Headers establish the context

`TX_BTC_HEADERS` carries Bitcoin headers into consensus. Nodes check header linkage, proof of work, difficulty rules and timestamp rules. Accumulated chainwork helps determine the accepted branch under the protocol's header validation rules.

The resulting view is shared input to contract evaluation. A script uses the protocol's defined snapshot and readable history, rather than whichever tip an application happens to observe on an external server.

Header verification is distinct from a full execution of every Bitcoin transaction. The supported contract predicates consume the specific evidence defined for them. Applications should describe that evidence precisely rather than treating the header database as an arbitrary Bitcoin query service.

## Prove a payment

A payment proof supplies the transaction and a Merkle branch linking it to a block header. Verification connects the transaction to the header's Merkle root, checks the relevant destination and amount, and applies the required depth conditions.

Three questions remain separate: is the transaction included, does it contain the agreed payment, and is that evidence eligible for this condition? A transaction identifier answers none of these on its own.

[Bitcoin facts in contracts](bitcoin-facts.md) introduces the supported predicates. Difficulty, height and median time use the accepted history; a confirmed payment additionally needs transaction evidence.

## Prove monetary origin

A burn claim identifies a Bitcoin output whose value is provably unspendable and binds the claim to the required BATHRON destination information. Nodes check the burn format, inclusion evidence, eligibility and uniqueness. An eligible verified claim permits the corresponding M0 creation through its dedicated transaction path.

The claim identifies the relevant Bitcoin transaction and output, so the same destruction cannot justify repeated issuance. Bitcoin used this way is destroyed, not transferred into a custodian's reserve.

## Track evidence through the application

Keep the proof data, referenced outputs and expected condition with the agreement. Distinguish a newly observed Bitcoin event from evidence admitted by BATHRON's depth and validation rules. Track BATHRON transaction finality separately from Bitcoin observation.

Proof of a payment can satisfy a local contract condition. The [trust boundaries](trust.md) distinguish that verification from external execution.

See [RPC and transactions](rpc-transactions.md) for submission and inspection, [Monetary invariants](invariants.md) for origin accounting and [Contracts on Bitcoin facts](bitcoin-contracts.md) for application examples.
