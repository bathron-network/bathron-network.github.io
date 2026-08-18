# Conditional escrow

Many trades are not "pay now, receive now": payment depends on a second leg, a deadline or an
event that has to be proven. Today that means an escrow agent who holds the money and whom both
sides must trust. On BATHRON the escrow is a covenant: it releases when the condition is proven
and refunds when the timeout passes, and no agent holds the principal in between. Lightning and
plain Bitcoin transactions remain the better choice for ordinary payments; this pattern starts
only where a condition is attached.

## The flow

A Clearing Provider quotes an execution path and a timeout path in the client's familiar assets
— amount, fees, deadline, refund route. Liquidity Provider inventory funds the conditional M1
leg. A proven event releases the settlement; if it does not occur, the client's commitment
follows the specified refund path.

```text
client BTC commitment -> quoted condition
                             | condition proven
                             v
                    CP/LP internal covenant -> recipient leg
                             |
                             +-- timeout -> client refund path
```

The client is not asked to hold or spend M0/M1; the condition is evaluated in BATHRON's
settlement state, and the client sees only the quoted BTC path.

## Conditions a covenant can check

- a **confirmed Bitcoin payment** — `TX_CONFIRMED` proves the payment is buried under the
  in-consensus header chain;
- a **designated signature** — `CSFS` verifies a signature from a named key over agreed data;
- an **expiry** — `CSV`/`CLTV` enforce the timeout;
- a **forced destination** — `CTV` constrains where the released funds may go.

## What must be defined

Every execution and refund branch has to be spelled out — Bitcoin-side timelock ordering,
reorganisation handling, wallet verification — before a flow can promise that no agent can take
the principal. That specification is a design target, not a current general guarantee; see
[Status & claims](../../consensus/status-and-claims.md).

**Primitives:** `TX_CONFIRMED` · `CTV` · `CSV` / `CLTV` · `CSFS` · confidential internal
transfers

**See also:** [Build your first application](../../operate/first-application.md)
