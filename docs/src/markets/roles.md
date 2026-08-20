# Roles: Operators, Settlement Providers, users

A market only stays open to everyone if the people who run consensus are not the people who
choose which markets exist or who gets to serve them. BATHRON keeps those functions apart:
Operators settle, Settlement Providers compete, users build and settle. Knowing which role does
what tells you who you depend on — and who you do not.

## Three roles, one table

| Role | What it does | Main risk |
|---|---|---|
| **Operator** (Settlement Operator) | produces blocks, signs finality, publishes Bitcoin facts inside consensus | operational and consensus participation |
| **Settlement Provider — Clearing Provider (CP)** | quotes a client, orchestrates the legs, sets deadlines and SLA | execution and service risk |
| **Settlement Provider — Liquidity Provider (LP)** | holds inventory, prices a pair, earns the spread | capital, market and liquidity risk |
| **User** | builds a market, builds an application, or simply settles | whatever the chosen route carries |

One company may perform several roles; the protocol never requires that they be bundled, and it
does not prove that an Operator and a provider are the same entity.

```text
                    ┌──────────────────────────────┐
                    │  Operators (consensus)       │
                    │  produce · finalize          │
                    │  publish Bitcoin facts       │
                    └──────────────┬───────────────┘
                                   │ publish facts
                                   ▼
             ┌────────────────────────────────────────────┐
             │  BATHRON settlement state (M1, covenants)  │
             └───────┬──────────────────────────┬─────────┘
                     │ settle                   │ settle
                     ▼                          ▼
      ┌──────────────────────────┐    ┌──────────────────────────┐
      │  Settlement Providers    │    │  Users                   │
      │  CP: quote, orchestrate  │◄───│  build a market, build   │
      │  LP: inventory, spread   │quote│  an app, or just settle  │
      └──────────────────────────┘    └──────────────────────────┘
```

There is no arrow from Operators to providers or users. Operators publish facts; they do not
select, rank or approve anyone.

## Operators: consensus, nothing more

Operators produce blocks, sign finality certificates and carry Bitcoin headers and proofs into
consensus. One operator identity has one vote; the protocol publishes facts and never a ranking.
Operators do not decide which pairs may exist, do not pick which provider serves a client, and
cannot create M0 without a verified Bitcoin destruction (see
[Security model](../consensus/security-model.md)).

> Anyone can build, quote, pair and settle on BATHRON without asking permission. Operator
> admission is **not yet open**: the current operator set is project-run while the
> open-admission threat model is worked.

## Settlement Providers: the commercial layer

Settlement Providers are participants, never administrators. They appear when someone brings
inventory and quotes, and disappear when they stop; the protocol neither selects nor licenses
them.

- The **Clearing Provider** faces the client: it quotes amount, deadline, fees and refund path
  in the client's familiar assets, then orchestrates the legs of the settlement.
- The **Liquidity Provider** faces the market: it holds inventory in M1 and in the paired
  asset, prices the pair, and takes the inventory risk.

Choosing or pinning a provider establishes a service route. It does not create a private
consensus committee and does not replace the global finality set.

## Users

Anyone who builds a market, builds an application on the covenant surface, or just settles a
trade. End users settle in the assets they already hold; market builders and providers settle
in M1.

## How providers are paid

The CP charges explicit service fees. LPs set spreads against inventory acquisition, liquidity,
capital and operating costs. Competition may compress prices, but the protocol does not guarantee
liquidity, a price near par, or that any spread covers any cost.

The Bitcoin-destruction route is one way an LP can acquire M1 inventory. **The destruction is
irreversible**: the bitcoin is gone and nothing in the protocol returns it. What the burn produces
is a transferable M0/M1 position that may carry a market value — a value the protocol neither sets,
supports nor predicts. Whether service revenue ever covers the cost is a commercial question, and
this documentation makes no claim either way. Expected appreciation of M0 or M1 is not a business
model.

Quoting and LP software exist as testnet prototypes; see
[Status & claims](../consensus/status-and-claims.md).

**See also:** [How a market appears](how-a-market-appears.md) ·
[Create your first market](../operate/create-your-first-market.md)
