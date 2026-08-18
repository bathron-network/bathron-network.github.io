# The settlement unit: M1

A market needs a unit to settle in. Not a coin to speculate on — a **numéraire**: one common
measure so that every pair, every escrow and every hedge on the network is expressed the same way
and can be netted against every other. That unit is M1. This page says what it is, where it comes
from, who touches it, and what it is not.

## Why one unit, and not one per market

Without a common unit, N assets need N² pairs, each with its own thin liquidity. With one, they
need N pairs around a single hub — the same reason foreign-exchange markets pivot through a few
currencies and the same reason a common language beats pairwise translation.

```text
        PIVX/M1        DOGE/M1        LTC/M1
             \            |            /
              \           |           /
                ──────  M1  ──────  ◄── the hub every pair settles through
                          |
                       BTC/M1        ◄── the deepest pair: native BTC in and out
```

M1 is that hub. Every settlement pattern in part III — DvP, escrow, hedge, fixed-term value — is
written in M1 so that a Liquidity Provider can hold one inventory and quote many pairs.

## Where M1 comes from

```text
BTC  ──(irreversible, SPV-proven destruction)──►  M0  ──(lock, 1:1)──►  M1
                                                       ◄─(unlock, 1:1)─
```

- **M0** exists only when bitcoin has been provably destroyed on the Bitcoin chain and the proof
  has been verified inside BATHRON's consensus. One destroyed satoshi permits one M0 unit; there is
  no premine, no block reward, no treasury, no issuer, no genesis exception.
- **M1** is M0 vaulted 1:1: the programmable receipt that covenants can lock and release. Locking
  and unlocking are free protocol operations; the vaulted M0 always equals the M1 supply.

Both rules are consensus invariants (A5 and A6) that every node checks on every block. A finality
quorum can order transactions; it cannot create a unit. → [From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)

## Who touches M1

End users settle in the assets they already hold; market builders and providers settle in M1.

A person swapping DOGE for BTC through a provider sees DOGE go out and BTC come in. The provider,
the market builder, the dealer quoting a pair — they hold M1 inventory, because M1 is what the
consensus can lock, release, hedge and net. Nobody is asked to "buy M1" as a product; it is the
working capital of whoever runs a market.

## What M1 is not

- **Not a coin with an issuer.** Nobody can print it and nobody can freeze it.
- **Not pegged.** Consensus enforces the internal 1:1 between M0 and M1. It does not enforce, and
  the protocol never promises, an external price against BTC. The destroyed bitcoin is gone; there
  is no reserve and no redemption desk. What makes native BTC available again is the market —
  providers holding inventory on both sides, paired with linked hashlocked legs
  (→ [Native BTC ⇄ M1](../markets/native-btc-pair.md)).
- **Not an investment.** Anyone can create M1 by destroying bitcoin, so destruction is a
  permanent *reference supply route*: when it is accessible, it tends to limit any premium over
  the cost of creation — there is nothing to speculate up. It is not a hard ceiling (arbitrage
  has fees, confirmation delay, inclusion risk and illiquidity), and there is **no floor**:
  demand for settlement — inventory, collateral, working capital — is what markets built on top
  must create, and it guarantees no price. The protocol guarantees the unit's integrity, never
  its value.

The realizable value of M1 for a professional depends on available liquidity and can be heavily
discounted; see [Status & claims](../consensus/status-and-claims.md) for what is and is not
promised.

**Next:** [Settlement guarantees: what consensus enforces](settlement-guarantees.md)
