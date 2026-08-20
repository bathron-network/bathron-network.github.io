# What BATHRON deliberately does not do

> Bitcoin does not decide who may hold BTC. BATHRON does not decide which markets may exist.

The most important design decisions of this protocol are the things it refuses to do. Each item
below is a boundary, not a missing feature — the consensus stays small so that the markets on top
of it can be free.

## Not in the protocol, on purpose

| BATHRON has… | …because |
|---|---|
| **no order book** | matching is a market-layer job; a book in consensus would make the protocol the exchange it refuses to be |
| **no matching engine** | same reason — and it would fix a single mechanism for all markets |
| **no listing process** | a market exists when someone brings inventory and quotes; nobody grants that, so nobody can revoke it |
| **no published price** | consensus does not know prices; it settles at whatever the parties agreed off-chain |
| **no chosen market maker** | operators publish facts about themselves and never rank anyone; providers compete on price and are chosen by users and applications, not by the protocol |
| **no token sale, premine, treasury or block reward** | M0 comes only from verified Bitcoin destruction; the coinbase equals the block's fees, nothing more |
| **no promised yield** | there is nothing to pay it from and nothing to vote it into existence |
| **no issuer, no freeze list, no redemption desk** | the burn is one-way; nobody holds a reserve, so nobody can gate access to it |
| **no slashing** | deterrence is the up-front cost of acquiring M0 collateral plus loss of eligibility; a slashing bug can destroy honest operators' funds — this will not be reconsidered |
| **no protocol ranking of operators or providers** | the protocol publishes facts (age, blocks produced, service history) and never a judgement; 1 operator = 1 vote |
| **no general-purpose VM** | scripts terminate and stay auditable; the covenant surface is frozen |

## What the consensus does instead

It settles. It keeps the accounts, verifies Bitcoin facts, evaluates the conditions written into
covenants, and finalizes transfers. → [Settlement guarantees](settlement-guarantees.md)

## Why the negative list is the product

Every item above is a place where a protocol *could* have taken power — over which pairs exist,
who makes markets, what a unit is worth — and chose not to. That refusal is what makes the
following sentence true: **markets belong to whoever builds them.** A protocol that lists cannot
be neutral about listing; a protocol that ranks cannot be neutral about providers; a protocol
that mints cannot be neutral about value.

The consensus surface is frozen **as it stands today** — a governance decision on the current surface, not a property of the code and not a promise about every future version — so that this list stays true. Any future value must be built above it —
which is exactly what part III describes.

**Next:** [How a market appears](../markets/how-a-market-appears.md)
**See also:** [Why the consensus is frozen](../consensus/why-frozen.md)
