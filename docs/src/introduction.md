# What is BATHRON?

BATHRON is a **settlement kernel for Bitcoin**.

It provides a shared settlement state anchored to Bitcoin.

- **Bitcoin remains the source of truth.** The chain reads Bitcoin — headers, payments, difficulty — inside consensus, with no oracle and no federation.
- **Consensus maintains the settlement state.** Deterministic block production, BFT finality in about a minute, private transfers.
- **An open market provides native BTC liquidity.** Settlement Providers compete on fees. The protocol never sells anything.

BATHRON is infrastructure. Applications are built on top of it.

<svg viewBox="0 0 640 158" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A shared settlement state anchored by Bitcoin">
  <rect x="80" y="8" width="480" height="80" rx="14" fill="#0C0F14" stroke="#1C222C"/>
  <text x="320" y="32" text-anchor="middle" fill="#D9A441" letter-spacing="3" font-family="ui-monospace,Menlo,monospace" font-size="12" font-weight="600">BATHRON</text>
  <text x="320" y="54" text-anchor="middle" fill="#E8EBF0" font-family="ui-monospace,Menlo,monospace" font-size="14">shared settlement state</text>
  <text x="320" y="76" text-anchor="middle" fill="#8A919C" font-family="ui-monospace,Menlo,monospace" font-size="13">Applications · SDK · Wallets · Settlement Providers</text>
  <line x1="42" y1="120" x2="598" y2="120" stroke="#D9A441" stroke-width="2" opacity=".55"/>
  <rect x="16" y="108" width="24" height="24" rx="6" fill="#D9A441"/>
  <rect x="600" y="108" width="24" height="24" rx="6" fill="#D9A441"/>
  <text x="28" y="154" text-anchor="middle" fill="#8A919C" font-family="ui-monospace,Menlo,monospace" font-size="13">BTC</text>
  <text x="612" y="154" text-anchor="middle" fill="#8A919C" font-family="ui-monospace,Menlo,monospace" font-size="13">BTC</text>
</svg>

## Where to go next

- **[Getting Started](getting-started/run-a-node.md)** — run a node, run a wallet, build on the chain.
- **Learn** — how the pieces fit together, starting with the [architecture](learn/architecture.md). No code.
- **Build** — the [SDK](build/sdk.md) and [RPC API](build/api.md) for developers.
- **Reference** — the details: [transaction types](reference/transaction-types.md), [opcodes](reference/opcodes.md), [invariants](reference/invariants.md).
- **[Understanding BATHRON — a calm essay](essay.md)** — a long-form explanation of the whole mechanism: what exists in code, what is a design goal, and what remains an open market question. Aussi disponible [en français](essai-fr.md).

> **Status: experimental.** A private testnet is running the full, frozen consensus surface; a public testnet is next. The path — and the honest open-network work before any mainnet — is on the **[Roadmap](roadmap.md)**.
