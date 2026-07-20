# Application hypotheses

These are possible compositions of the protocol primitives, not shipped products or promises.

| Application | Conditional settlement being tested |
|---|---|
| [Delivery versus payment](applications/dvp.md) | release one leg only when delivery is proven |
| [Escrow](applications/escrow.md) | execute or refund under explicit conditions and timeouts |
| [OTC settlement](applications/otc.md) | coordinate quoted bilateral legs |
| [Conditional BTC settlement](applications/payments.md) | add a verifiable condition to a BTC payment |
| [Provider inventory controls](applications/vaults.md) | constrain CP/LP treasury movement |
| [Miner hedging](applications/miner-hedging.md) | settle against Bitcoin difficulty facts |
| [Fixed-term value position](applications/stable-value.md) | bilateral outcome using an explicit oracle |

Ordinary payments and personal wealth storage are not the thesis. The acceptance test is whether
a CP can deliver useful conditional settlement in the client's familiar assets and fund the
service through disclosed fees and spreads.
