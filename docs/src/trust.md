# Where trust lives

An agreement becomes easier to judge when its dependencies have names. Instead of calling a whole application trustless, say whom you rely on, for what, and for how long. BATHRON makes some conditions independently verifiable and leaves other responsibilities with the people who provide the service.

## Begin with the condition

Consider a payment released after another payment arrives on Bitcoin. BATHRON nodes can check a transaction proof against their accepted Bitcoin header view. The recipient need not appoint a person to report that Bitcoin event. Someone still prepares the proof and submits the spending transaction.

Now consider payment after a machine reaches a factory. Bitcoin cannot prove delivery. The agreement needs an attestation, an arbitrator or another external process. A valid signature authenticates the statement's source; it does not establish that the machine arrived in the promised condition.

## Locate each responsibility

| Layer | What participants rely on |
|---|---|
| Bitcoin | Its chain rules and the evidence used to establish Bitcoin facts |
| BATHRON | Validation of accounting, scripts, Bitcoin evidence and finality |
| Provider | Inventory, quote terms, external execution and monitoring |
| Application | Correct transaction construction and understandable recovery paths |
| Attestation source | The meaning, accuracy and availability of an external statement |
| User | Key control, consent to terms and any assigned monitoring duties |

These dependencies have different durations. A provider's quote can expire quickly. A funded contract can remain open until its recovery condition is satisfied. An attestation may matter only at a specified observation point. The application should show these periods before funding.

## Operator identity and accountability

An Operator identity requires a burned ticket and maturity. Its entry cost is real, visible and permanently spent. Objectively proven double signing results in a permanent ban of the identity, with no slashing; the burned ticket is not recoverable. An SP carries this identity even when it does not produce blocks. Identity accountability and commercial service quality remain separate questions.

## Why not Lightning, Liquid or DLCs on Bitcoin?

These mechanisms address different needs, and can be appropriate without BATHRON:

### Lightning

**What it does well:** Moves Bitcoin payments off-chain through linked payment channels. See the [Lightning documentation](https://lightning.network/docs/).

**What BATHRON adds:** Contracts can require a Bitcoin height, difficulty threshold or confirmed payment that every BATHRON node verifies in consensus, without an oracle reporting that Bitcoin fact.

### Liquid

**What it does well:** Provides asset issuance and transfers with hidden amounts and asset types on a federated Bitcoin sidechain. See the [Liquid technical overview](https://docs.liquid.net/docs/technical-overview).

**What BATHRON adds:** M1 provides a common settlement unit for independent providers quoting BTC/M1 or any asset against M1. Market creation needs no listing permission; providers supply the external inventory and execution under the [requirements of their role](roles.md).

### DLCs on Bitcoin

**What they do well:** Let parties agree Bitcoin payouts tied to an oracle's signed outcome, with a refund path if the outcome is unavailable. See the [DLC specification introduction](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Introduction.md).

**What BATHRON adds:** Builders can compose authorization, evidence, deadlines and constraints on successor outputs in shared settlement rules. Parties who do not know each other can inspect those rules before funding. Supported Bitcoin facts are checked directly in consensus; a dollar price or a physical delivery still needs an external source.

Choosing BATHRON also means relying on its own consensus and holding or using its internal units, alongside the dependencies of each external leg. These are different constructions, not interchangeable guarantees.

## Privacy and economic boundaries

Shielding protects M0 transfer details. It does not hide M1 receipts, conditional exchanges, burn or lock/unlock operations, or erase information exposed through entry and exit points, counterparties and application records.

A BTC burn is irreversible and creates no redeemable Bitcoin reserve. Unlocking M1 returns M0, not BTC. The one-for-one M0/M1 relationship sets no external price floor or fixed exchange rate. A possible pair is not available liquidity: it needs providers, executable quotes and funded inventory on each leg. Demand, spreads and returns depend on participants and their economic arrangements.

BATHRON consensus and M1 are shared dependencies across applications; using several providers does not remove those common risks. Cross-chain recovery depends on each chain's rules and progress, correctly ordered deadlines, retained keys and data, and timely transaction inclusion. Compatible hashlocks alone do not establish universal atomicity.

## Compare mechanisms by what they control

A custodian controls funds under its keys. A contract constrains spends through rules visible to participants. A relay helps find offers. An indexer organizes observations. A human arbitrator judges facts that a script cannot interpret. Each can be useful when its authority matches the agreement.

BATHRON reads Bitcoin; it never commands it. Finality on BATHRON does not move an external asset. For a trade across chains, the external leg follows its own rules and the provider's execution process. [Settlement across chains](cross-chain.md) makes that division explicit.

## Make recovery an action

A refund right is useful only if someone's software watches the chain and acts on it. Record who keeps the required data, who can sign, when a path opens, and who pays for inclusion. A deadline is a condition for a transaction, not a scheduled transfer that executes itself.

The practical question is whether each dependency is acceptable for this agreement. Use [What consensus enforces](boundaries.md) to identify the protocol's part, then read the application's own terms for the rest.
