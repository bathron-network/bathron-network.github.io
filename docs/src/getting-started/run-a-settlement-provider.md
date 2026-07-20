# Run provider prototypes

The testnet separates two commercial responsibilities:

- a **Clearing Provider (CP)** exposes quotes and orchestrates execution and timeout paths;
- a **Liquidity Provider (LP)** holds inventory and prices a pair.

One operator can run both prototypes, but production architecture may aggregate several LPs.

| Component | Purpose |
|---|---|
| BATHRON full node | validate and settle internal state |
| Bitcoin wallet | fund quoted external legs |
| CP service | quotes, workflow state and SLA |
| LP service | inventory, pair pricing and risk limits |

The current software demonstrates quoting and individual settlement components. It must not yet be
represented as a generally atomic or risk-free client service: reorganisation handling, timelock
ordering and all failure transitions require a formal specification and external review.

Provider revenue is explicit fees and spread. Provider risk includes irreversible inventory
acquisition, liquidity, pricing, operations and software failure.

Interested in evaluating the economics? [Contact us](mailto:contact@bathron.org).
