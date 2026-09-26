# Who does what

A user should be able to tell who validates the protocol, who supplies inventory and who builds the interface. These jobs can belong to the same organization, but they remain different responsibilities. BATHRON separates consensus participation from commercial services and application design.

The guiding division is simple: BATHRON provides settlement; providers operate the edges; third parties build the applications.

## Six roles

| Role | Responsibility | Operator identity |
|---|---|---|
| Operator | Participate in the network's consensus functions | Required for that role |
| Settlement Provider, SP | Quote and arrange BTC/M1 settlement, including the Bitcoin leg | Required; block production is optional |
| Liquidity Provider, LP | Supply X/M1 liquidity and manage the external asset leg | Optional |
| Builder | Create agreements, wallets, interfaces and application services | Not required to build |
| User | Choose terms, authorize operations and receive the service | Not required to use an application |
| Observer | Independently verify history and publish observations | Not required to observe |

An Operator is a registered identity based on a burned ticket and maturity; one Operator, one vote; it may produce blocks and sign finality. Its burned ticket is a real, visible and permanently spent entry cost. It gives service history an identifiable subject and carries protocol accountability. Holding that identity and producing blocks are separate matters: an SP can carry the identity without acting as a block producer.

## Providers operate the edges

The SP specializes in BTC/M1. Its work includes inventory, quotes, orchestration, deadlines and Bitcoin execution. The LP specializes in X/M1 and handles the external asset and its chain-specific requirements. An application can combine their services into a route chosen for a customer.

Neither role is a listing authority. A quote is an offer from a provider, not an official protocol price. Customers and applications decide which offers to use.

## Multiple roles remain visible

An Operator can also run a provider business. The relationship between the registered identity and the advertised service is public. Transactions follow the same validity rules whoever submits them.

A builder can run discovery services, or users can connect directly to providers. An observer can publish service history without quoting any market. Keeping these roles distinct lets users evaluate each service on its own evidence.

Protocol accountability means a permanent ban for objectively proven double signing; no slashing. The burned identity ticket remains spent.

## Reputation is an interpretation

Published facts can include identities, signed offers and observable service history. Users, wallets and independent services interpret those facts. Consensus does not assign a commercial reputation score or select a preferred provider.

An identity identifies a participant; it does not guarantee a price, inventory or service outcome. An observer's report is useful because its evidence can be examined, not because the observer gains authority over settlement.

Continue with [Network operators](operators.md), [Operate a provider](providers.md) or [Run and observe a node](node.md), depending on the responsibility you want to understand.
