# Create your first market

A market on BATHRON is a pair `X/M1` that exists the moment someone brings inventory in `X`
and in M1 and starts quoting. There is no listing form, no committee and no fee to pay
anyone: the protocol never validates a pair, and Operators cannot approve or refuse one. This
page walks through what you need and the four steps from inventory to a live market.

## What you need

| Component | Purpose |
|---|---|
| **BATHRON full node** | validate and settle the M1 side yourself ([Run a node](run-a-node.md)) |
| **Inventory in the paired asset** | the `X` side of `X/M1` — for a BTC pair, native bitcoin |
| **M1 inventory** | acquired from an existing holder, or through the burn route ([From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)) — irreversible, so price it as a cost |
| **A Bitcoin wallet** | if the pair is BTC: fund and claim the Bitcoin leg of each settlement |
| **CP / LP software** | quotes, orchestration, inventory and risk limits (see below) |

Provider revenue is explicit fees and spread. Provider risk includes irreversible inventory
acquisition, liquidity, pricing, operations and software failure — see
[Roles](../markets/roles.md).

## The prototypes

Two **historical prototypes, decommissioned** — their state belonged to a superseded network and
neither service is running. They are read as illustrations of the two commercial roles, not as
software to point at:

- **`pna-lp`** — a Liquidity Provider service. It holds inventory, prices a pair and exposes
  quotes over plain HTTP: `GET /api/status` for health, and
  `GET /api/quote?from=…&to=…&amount=…` for a price on a given amount and direction.
- **`pna-swap`** — the swap UI. It reads quotes from one or more LP endpoints and drives a
  settlement from the client's side.

One participant can run both, but a Clearing Provider may aggregate several LPs; the protocol
does not care how they are arranged.

## The four steps

1. **Bring inventory.** Fund your BATHRON wallet with M1 ([Run a wallet](run-a-wallet.md))
   and your Bitcoin (or other) wallet with the paired asset.
2. **Publish quotes.** Run `pna-lp` (or your own service) and expose `/api/quote` for your
   pair. Quotes live off-chain ([Quotes live off-chain, settlement on-chain](../markets/quotes-off-chain.md));
   nothing is written to the chain until someone settles.
3. **A counterparty settles.** A client accepts a quote; the two legs are locked and settled
   with the [atomic pair](../markets/native-btc-pair.md) or one of the
   [settlement patterns](../markets/patterns.md). Consensus enforces the outcome.
4. **Others join.** Anyone else can quote the same pair, aggregate your quotes, or pair a new
   asset. Nobody approves the pair; competition sets the spread.

The current software demonstrates quoting and individual settlement components; it must not be
represented as a generally atomic or risk-free client service — see
[Status & claims](../consensus/status-and-claims.md).

Interested in evaluating the economics? [Contact us](mailto:contact@bathron.org).

**See also:** [How a market appears](../markets/how-a-market-appears.md) ·
[Pairing an external asset against M1](../markets/pairing-any-asset.md) ·
[Patterns for providers](../reference/patterns-for-providers.md)
