# Monetary invariants

BATHRON's monetary rules establish provenance and conservation. They answer where internal units originate and how their representations remain balanced. Market exchange is a separate operation.

The distinction matters whenever an application presents M0 or M1 to a participant. An internal accounting equality and an executable market quote are different facts, supported by different evidence.

## Provenance of M0

Every M0 unit originates from verified Bitcoin destruction. The accounting relationship uses corresponding base units:

```text
M0 total = BTC destruction recognized by completed M0 issuance
```

A claim requires the prescribed evidence, eligibility and maturity checks. An admissible claim permits issuance; M0 enters supply only when the dedicated mint transaction is applied. Reusing a burn output does not create another entitlement to issuance. Transferring M0 changes its owner without creating new origin.

There is no premine, issuer allocation or block subsidy in this origin rule. Block production does not independently create monetary units. Transaction fees move existing value under the fee rules.

The provenance relation records irreversible origin.

## Conservation between M0 and M1

Locking M0 vaults it and creates corresponding M1 receipts. Unlocking consumes those receipts and releases the matching M0. The accounting equality is:

```text
Vaulted M0 = outstanding M1 supply
```

M0 represented by an outstanding receipt is not simultaneously free inventory. Counting both as independently spendable funds would misread the same underlying accounting position.

A receipt transfer changes ownership without increasing supply. Dedicated settlement transaction types enforce these transitions. See [RPC and transactions](rpc-transactions.md) for the operations involved.

## Fee conservation

Network transaction fees move existing value. The coinbase contains the block's M0 fees, with no block subsidy. Fees routed through M1 receipts remain subject to receipt accounting; they are not new M0 issuance.

## Conservation in the shielded pool

Shielded M0 transfers use proofs to enforce conservation across shielded and transparent value, including fees, without publishing protected amounts. Shielding creates no new units. See [Private inventory transfers](confidentiality.md).

## Validation precedes finality

Every validating node checks the monetary rules. A producer's proposal or an Operator signature does not authorize a transaction to bypass them. Finality applies to validated history; it is not a separate source of permission to issue or spend funds.

Wallets and providers reconcile their records against these state transitions. They distinguish available M0, vaulted M0, held receipts and funds committed to an agreement. A displayed total should explain which categories it includes.

[M1: the settlement pivot](m1.md) explains the two representations and their use in settlement. [Bitcoin verification](bitcoin-verification.md) describes origin evidence; [Where trust lives](trust.md) covers economic boundaries.
