# Why not an exchange, a bridge, or a stablecoin

Each of the usual answers solves part of the problem by giving up something BATHRON refuses to
give up. This page is not a claim of superiority — every system below is useful for someone. It
is a map of the trade-offs, so you can see which one BATHRON signs.

## The three constraints again

A place to settle a market must (1) hold nobody's funds in custody, (2) verify Bitcoin facts
without a designated oracle, and (3) be open — no admission, no listing.

| | Custody-free | Verifies Bitcoin itself | Open — no listing |
|---|---|---|---|
| Centralised exchange | no | n/a | **no** — the listing committee *is* the product |
| Custodial or federated bridge | **no** — someone holds the reserve | usually not | partly |
| Fiat stablecoin | **no** — an issuer holds the reserve | no | partly |
| Lightning | yes | yes | yes — but payments only, no rich conditions |
| Multisig + human arbiter | mostly | no | yes — but does not scale, needs interpretation |
| **BATHRON** | yes — the burn is one-way, nothing is held | yes — headers and proofs in consensus | yes — for markets, builders and providers today; operator admission not yet |

## Exchanges: the permission problem itself

An exchange gives you liquidity, custody and customer service — against holding your funds and
deciding which markets exist. Its listing committee is not a bug; it is the business. If your
problem is *"who decides my market exists"*, an exchange is the problem, not the answer.

## Bridges: trusted by whom, for what, for how long

Lock bitcoin on one side, mint a representation on the other, do there what Bitcoin forbids, come
back — every bridge raises one question: *while you are on the other side, who holds your
bitcoin?* A custodian is a keeper. A federation is a group of keepers — better, one key is no
longer enough, but the reserve still exists and identifiable actors control it. Optimistic designs
do better still, and still rest on a setup ceremony and watchers who stay alive and funded.

None of this is absurd. But never call it trustless: say **whom** the user trusts, **for what**,
**for how long** — and the answer always contains a keeper, because the original bitcoin still
exists and somebody holds it.

BATHRON's choice is radical and has a cost: **the bitcoin is destroyed, verifiably, and never
held.** There is no keeper — and therefore no reserve and no redemption. What brings native BTC
back is not a vault but a market: providers holding inventory on both sides, paired with linked hashlocked legs.
That is the trade-off you sign. It is stated plainly on
[Bitcoin is the final asset](../bitcoin/final-asset.md).

## Stablecoins: an issuer by definition

A stablecoin is a claim on an issuer's reserve. It is the fastest way to a dollar balance and the
clearest example of what BATHRON is not: BATHRON has no issuer, no reserve, no redemption desk,
no freeze list. Value positions can be *built* on BATHRON (a bilateral, collateralised,
fixed-term contract priced by a professional — see
[Fixed-term value positions](../markets/patterns/fixed-term-value.md)) but the protocol mints
nothing that promises anything.

## Lightning and human arbitration: honest boundaries

**Lightning** is better for simple, fast payments — no contest, and BATHRON does not compete
there. Its subject begins where rich conditions are needed.

**A human arbiter** can look at photos, read messages, judge whether a product matched its
description. No covenant can do that. BATHRON targets **objectively verifiable conditions** — an
elapsed delay, a signature, a confirmed Bitcoin transaction. When the condition needs
interpretation, arbitration wins. This is the product's boundary, not a decorative concession.

## So what does BATHRON keep

Custody-free, Bitcoin-verifying, open. In exchange it gives up: a recoverable vault (so exit
liquidity must come from providers), simplicity (pre-committed transactions are more complex than
a database), and any promise about the price of its unit. Part II describes exactly what it
provides in return.

**Next:** [The settlement unit: M1](../provides/settlement-unit-m1.md)
