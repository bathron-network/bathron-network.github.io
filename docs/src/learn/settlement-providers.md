# Settlement Providers

Ten seconds of mechanism first:

```text
        Alice                          Settlement Provider
          │                                     │
          │  wants native BTC                   │  quotes a price
          │                                     │
          ▼                                     ▼
          ────────────  the swap  ───────────────
          │                                     │
   Alice pays on the                   SP pays native BTC
   settlement state                    on Bitcoin
          │                                     │
          └────────── one shared secret ────────┘
                 claiming either leg reveals it —
                 both legs settle, or neither does
```

No custody, no credit, no counterparty risk: an unfinished swap refunds, it does not lose money.

## Who are Settlement Providers?

Market makers. Anyone holding native BTC who wants to earn a spread can quote prices for moving value between Bitcoin and the settlement state. There is no license, no whitelist, no protocol-blessed operator.

## Why do they exist?

Because the protocol refuses to do their job. BATHRON can *read* and *consume* Bitcoin but cannot *move* it — so native BTC liquidity must come from someone who has it. Making that someone an **open, competing market** (rather than a federation, a bridge, or the protocol itself) is a design decision: liquidity is an economic problem, and markets solve economic problems.

## How do they earn fees?

The spread between their quoted price and par. Competition between SPs compresses it. The protocol takes nothing.

## Liquidity and inventory

An SP manages two inventories — native BTC on one side, settlement-state value on the other — and rebalances via burns (in) and its own swaps (out). Pricing that inventory is the SP's actual craft; the protocol guarantees only that settlement is atomic.

## API and reference implementation

A reference SP — quoting service, swap API, dashboard — runs on the private testnet and will be published with the public testnet. The API surface is small: publish quotes, accept a swap, settle the legs.

Want to run one? [Contact us](mailto:contact@bathron.org).
