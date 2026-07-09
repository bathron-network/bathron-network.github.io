# Run a Settlement Provider

A Settlement Provider (SP) sells **native BTC liquidity** to users of the settlement state, competing on fees in an open market. The protocol never sells anything — SPs do. If you understand market making, you understand the role. Details: [Settlement Providers](../learn/settlement-providers.md).

## What an SP operates

| Component | Purpose |
|---|---|
| A BATHRON full node | validate the chain, hold inventory, settle |
| A Bitcoin wallet | the BTC side of quotes |
| The SP service | publish quotes, serve the swap API, manage inventory |

## The lifecycle of a quote

1. You publish a price for BTC ⇄ settlement-state value.
2. A user takes the quote.
3. The trustless machinery does the rest: the user's Bitcoin payment is **proven inside consensus** (SPV), a covenant releases the counter-payment, and the return leg settles as an atomic swap. You never custody user funds — and users never custody yours.

Your earnings are the spread. Your risk is inventory and pricing — not counterparty default: an unfinished swap refunds, it does not lose money.

## Reference implementation

A reference SP implementation (quoting service, swap API, dashboard) is running on the private testnet and will be published with the public testnet.

Interested in running one? [Contact us](mailto:contact@bathron.org).
