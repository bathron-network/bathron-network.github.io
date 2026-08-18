# How a market appears

On an exchange, a market appears when a committee approves it. On BATHRON, a market appears when
someone can settle it. This page walks through that moment — who does what, who pays what, and
where the protocol stops.

## Four steps, no gate

```text
  1. INVENTORY            2. QUOTES                3. SETTLEMENT           4. OTHERS JOIN
  ────────────            ─────────                ─────────────           ─────────────
  someone holds           publishes signed          a counterparty          another provider
  the asset (PIVX,        bid/ask for               accepts; both legs      quotes the same
  DOGE, LTC, BTC…)        PIVX/M1 — off-chain,      settle on BATHRON       pair, tighter,
  and M1                  on any relay              (the only on-chain step) or deeper
        │                       │                        │                       │
        └───────────────────────┴────────────────────────┴───────────────────────┘
                     nobody approves any of it — the protocol only settles step 3
```

**Step 1 — inventory.** A market maker holds the asset to be paired and M1. M1 is acquired
either from an existing holder or by the one-way route (destroy BTC, receive M0, lock it into M1
— → [From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)). That cost is real and irreversible;
it is recovered through spreads and fees, never through appreciation.

**Step 2 — quotes.** The maker publishes signed quotes: pair, bid, ask, size, expiry. They travel
off-chain — a relay, an HTTP endpoint, a message bus. The consensus never sees a quote and never
needs to. → [Quotes live off-chain](quotes-off-chain.md)

**Step 3 — settlement.** A taker accepts a quote. If the pair is BTC/M1, two hashlocked legs
settle atomically across the two chains; if the other asset lives on a chain with hashlocks and
timelocks, the same pattern applies; if it is an M1-denominated position (a hedge, an escrow),
a covenant settles it. This is the only step consensus performs, and it performs it identically
for every market.

**Step 4 — others join.** Nothing about the pair is registered, so nothing needs to be joined
"officially". A second provider publishes a tighter quote and the market has two makers. A third
arbitrages against an external venue. The pair deepens because it is profitable to deepen, not
because anyone was invited.

## Who pays what

| Party | Pays | Earns |
|---|---|---|
| Liquidity Provider | inventory cost (irreversible if acquired by burn), capital, market risk | the spread |
| Clearing Provider | orchestration, deadlines, service | explicit fees |
| Taker | the spread and fees, disclosed in the quote | the settlement it wanted |
| Operators | running consensus | block fees only — no reward, no subsidy |

Competition compresses spreads; the protocol guarantees none of it and takes none of it.

## What "no permission" means precisely

Anyone can build, quote, pair and settle on BATHRON without asking permission. Operator admission
is **not yet open**: the current operator set is project-run while the open-admission threat model
is worked. → [Status & claims](../consensus/status-and-claims.md)

The first half is a property of the design: the consensus does not know which pairs exist, so it
cannot gate them. The second half is where the network is today.

## What a market cannot do

It cannot make the protocol publish its price, favour its provider, or guarantee its liquidity.
A pair nobody quotes is simply silent — not delisted, silent — and it comes back the moment
someone quotes it again. Nobody can revoke what nobody granted.

**Next:** [Quotes live off-chain, settlement on-chain](quotes-off-chain.md)
