# Quotes live off-chain, settlement on-chain

The consensus never carries a price. That is not a limitation to be fixed — it is what keeps the
protocol neutral and the markets free. This page explains where quotes live instead, how a taker
finds them, and what the testnet prototypes already do.

## The split

```text
   OFF-CHAIN (yours)                              ON-CHAIN (consensus)
   ────────────────                               ────────────────────
   signed quote: pair · bid · ask · size · expiry      one settlement:
   relayed anywhere — HTTP, gossip, a chat, a file     hashlocked legs, or a covenant,
   aggregated by wallets and indexers                  final in ~1 minute
   compared, chosen, ignored                           identical for every market
              │
              └────────── the taker accepts ──────────►
```

A quote is a signed message. Anyone can publish one, anyone can relay one, anyone can aggregate
them. The consensus is involved exactly once: when the accepted quote becomes a settlement.

## Why not put the order book in consensus

Because a book in consensus is an exchange. It would fix one matching rule for every market, make
the protocol responsible for prices it cannot verify, and hand block producers a view of order
flow they could exploit. Keeping quotes off-chain means the protocol can be captured neither on
listing nor on price — it does not see either. → [What BATHRON does not do](../provides/what-it-does-not-do.md)

## How a taker finds a market

Discovery is a market-layer function and several mechanisms can coexist:

- **Announcements.** The testnet prototype lets a provider announce its endpoint with a plain
  `OP_RETURN` on BATHRON (`PNA|LP|01|<endpoint>`); any node can list announced providers. Nothing
  is validated by consensus — an announcement is a pointer, not a listing.
- **Relays and indexers.** Anyone can run a service that collects signed quotes and serves them;
  wallets connect to several, the way Bitcoin nodes connect to several peers.
- **Direct.** A wallet can be pointed at a provider's endpoint.

The taker then chooses — best price, best reputation, largest size, lowest latency. That choice
belongs to the wallet and the user, never to the protocol.

## What the prototypes already do

The Clearing/Liquidity Provider prototype (`pna-lp`) exposes quotes and settlement over HTTP:
`GET /api/quote?from=…&to=…&amount=…` returns a priced quote; `/api/status`, `/api/lps`,
`/api/reputation` expose provider state, announced providers and observable history; the swap
front-end (`pna-swap`) consumes them. Both are **testnet prototypes** published on the BATHRON
GitHub organization — an illustration of the split above, not a standard and not a product.
→ [Create your first market](../operate/create-your-first-market.md)

## The maker's real problem: the free option

A signed quote that a taker can accept "within N seconds" is an option the maker has written for
free: the taker will exercise it only when the price has moved in their favour. Every RFQ market
in the world has this problem, and none has eliminated it — it is **priced**: short expiries,
firm quotes only after the taker commits (a small collateral, a covenant), or a wider spread.
The primitives allow all three; which one a market uses is that market's business.

**Next:** [Roles: Operators, Settlement Providers, users](roles.md)
