# What is BATHRON?

BATHRON is an **experimental settlement kernel for Bitcoin**.

It tests a narrow proposition: when a Bitcoin transaction depends on a second payment, delivery
or deadline, can both legs be coordinated without giving one intermediary unrestricted custody?

- **Bitcoin facts are verified in consensus.** Headers and payment proofs are checked without an
  external oracle or federation.
- **BATHRON carries programmable settlement state.** Covenants, timelocks, confidential internal
  transfers and fast testnet finality express the conditions.
- **Professionals provide the service and liquidity.** Clearing Providers assemble quotes and
  execution paths; Liquidity Providers price inventory; Settlement Operators run consensus.

The client-facing product hypothesis is conditional settlement in familiar external assets—not
an internal coin. M0, M1 and Bitcoin destruction are back-office mechanics borne by professional
providers in the target model.

The testnet has demonstrated the main primitives, but the complete cross-chain safety model is
not yet formally specified or externally reviewed. There is no mainnet and no proven market.

## Where to go next

- **[Architecture](learn/architecture.md)** — how the pieces fit together.
- **[Clearing and liquidity providers](learn/settlement-providers.md)** — who supplies the service
  and who bears inventory risk.
- **[Delivery versus payment](learn/applications/dvp.md)** — the clearest target workflow.
- **[Getting Started](getting-started/run-a-node.md)** — run the experimental software.
- **[Build](build/sdk.md)** and **[Reference](reference/transaction-types.md)** — developer and
  protocol details.
- **[Roadmap](roadmap.md)** — what remains before any mainnet claim.
