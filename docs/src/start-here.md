# Start here — BATHRON in five minutes

Today a market exists because an exchange lists it, and it dies when the exchange delists it. Two
parties who both hold inventory still cannot settle against each other without handing custody to
a third. Bitcoin settles value beautifully — and deliberately refuses to express the conditions of
a trade.

BATHRON is built for exactly that gap.

## What BATHRON is

**An open settlement protocol.** It owns no market and no exchange, and it never decides which
assets may trade. It provides three things, and only three:

1. **A common settlement unit — M1.** Every settlement on the network is expressed in one
   numéraire. M1 is created only from verified, irreversible Bitcoin destruction; nobody issues it,
   nobody can print it.
2. **A consensus that guarantees settlement.** Accounting integrity, Bitcoin facts, the conditions
   written into contracts, and transfers — final in about a minute.
3. **An infrastructure any market can be built on.** Covenants, timelocks, hashlocks, Bitcoin-fact
   verification and confidential transfers, composable by anyone.

**Markets belong to whoever builds them.** A market on BATHRON exists because someone brings
inventory, publishes quotes and finds a counterparty — not because a committee allowed it.

**Bitcoin remains the final asset.** BATHRON does not replace Bitcoin, does not hold BTC, and does
not compete with it. It reads Bitcoin facts inside its own consensus and settles above it.

## What BATHRON deliberately does not do

No order book. No matching engine. No listing process. No published price. No chosen market
maker. No token sale, premine, treasury or promised yield. **The consensus only settles.
Everything else is yours.** → [What BATHRON does not do](provides/what-it-does-not-do.md)

## How a market appears

```text
1. someone brings inventory        (BTC, PIVX, DOGE, LTC… — and M1)
2. publishes signed quotes         (off-chain, on any relay — nobody approves them)
3. a counterparty settles          (M1 leg on BATHRON; an external leg on its own chain, linked)
4. anyone else joins the same pair (more inventory, tighter spreads — no permission asked)
```

Native BTC ⇄ M1 is paired with hashlocked legs on both chains sharing one preimage — the
components have been demonstrated on testnet; a generally atomic client flow is not yet claimed.
Any other chain that supports hashlocks and timelocks can be paired the same way — a capability
of the primitives, not a shipped product. → [How a market appears](markets/how-a-market-appears.md)

## Who is who

- **Operators** run consensus: produce blocks, sign finality, publish facts. One operator, one
  vote. They never rank, never choose a provider, never set a price.
- **Settlement Providers** are participants, not administrators: a Clearing Provider quotes and
  orchestrates, a Liquidity Provider holds inventory and prices a pair. They appear and disappear
  freely.
- **You** build a market, an application, or simply settle. End users settle in the assets they
  already hold; market builders and providers settle in M1.

## The permissionless sentence, both halves

Anyone can build, quote, pair and settle on BATHRON without asking permission. Operator admission
is **not yet open**: the current operator set is project-run while the open-admission threat model
is worked. → [Status & claims](consensus/status-and-claims.md)

## Where you are

Public testnet, live. No mainnet. No external audit yet. No proven market. That page above is the
only place these caveats are spelled out in full; every other page links to it.

## The sentence to take away

> BATHRON is an open settlement infrastructure where anyone can create a market without
> permission, while Bitcoin remains the ultimate settlement asset.

If that sentence is clear, continue with [The problem](problem/markets-need-permission.md). If you
want to run something, go to [Run a node](operate/run-a-node.md). If you want to build, start
with [The infrastructure](provides/infrastructure.md).
