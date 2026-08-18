# Settlement patterns

A market needs more than a spot exchange of two assets. Real settlement is conditional:
delivery against payment, funds released only when an event is proven, positions that pay out
on a Bitcoin fact or on a signed price. Each pattern below is a way to build one of those
conditions from the same primitives — hashlocks, timelocks, `CTV`, `CSFS`, `TX_CONFIRMED` — so
that a market builder does not have to trust an intermediary to hold the funds in between.

| Pattern | The condition it settles |
|---|---|
| [Delivery-versus-payment and OTC](patterns/dvp-otc.md) | both legs settle or neither does; size can stay hidden |
| [Conditional escrow](patterns/escrow.md) | execute on a proven event, refund on timeout, no agent holds the principal |
| [Hedging on Bitcoin facts](patterns/hedging.md) | a payout selected by Bitcoin difficulty read inside consensus |
| [Fixed-term value positions](patterns/fixed-term-value.md) | a bilateral, collateralised payoff on a signed reference price |

These are compositions of primitives that any market builder can assemble, not shipped
products. Each page lists its primitives; the covenant surface is documented in
[Script & opcodes](../reference/opcodes.md).

**See also:** [Native BTC ⇄ M1](native-btc-pair.md) ·
[Build your first application](../operate/first-application.md)
