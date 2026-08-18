# Bitcoin is the final asset

BATHRON exists to let markets settle without asking permission — but it does not exist to
replace the asset those markets ultimately care about. Bitcoin stays the reserve of value and
the only origin of the settlement unit. Getting this relationship right is what keeps BATHRON
from becoming one more custodian, bridge or issuer standing between a user and their BTC.

## What BATHRON is, relative to Bitcoin

BATHRON reads Bitcoin; it never commands it.

- It **never replaces** Bitcoin. Bitcoin is where value is held; BATHRON is where settlements
  between assets are made final.
- It **never holds BTC for redemption**. There is no vault of Bitcoin, no custodian, no address
  that "backs" anything.
- It **cannot move native BTC or trigger a Bitcoin transaction**. Consensus can verify Bitcoin
  facts — headers, proofs of inclusion, irreversible destructions — and that is the whole extent
  of the link ([Bitcoin facts inside consensus](facts-in-consensus.md)).

Bitcoin does not decide who may hold BTC; BATHRON does not decide which markets may exist. Both
sit underneath what people build, and neither one owns it.

## The link is one-way

The only way M1 comes into existence is by destroying BTC. Bitcoin is sent to a provably
unspendable output; every BATHRON node verifies the destruction against the Bitcoin header chain
it carries in consensus; one M0 unit is permitted per destroyed satoshi; M0 is vaulted 1:1 into
M1, the settlement unit.

<svg viewBox="0 0 640 118" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="BTC, one-way SPV-proven destruction, to M0, lock 1:1, to M1. No reserve, no redemption.">
  <g font-family="ui-monospace,Menlo,monospace" font-size="12">
    <rect x="16" y="34" width="96" height="40" rx="6" fill="#0C0F14" stroke="#1C222C" stroke-width="2"/>
    <text x="64" y="59" text-anchor="middle" fill="#D9A441" font-weight="600" font-size="14">BTC</text>
    <line x1="112" y1="54" x2="330" y2="54" stroke="#D9A441" stroke-width="2"/>
    <polygon points="330,49 342,54 330,59" fill="#D9A441"/>
    <text x="222" y="30" text-anchor="middle" fill="#8A919C" font-size="11">one-way, SPV-proven destruction</text>
    <rect x="342" y="34" width="72" height="40" rx="6" fill="#0C0F14" stroke="#1C222C" stroke-width="2"/>
    <text x="378" y="59" text-anchor="middle" fill="#E8EBF0" font-weight="600" font-size="14">M0</text>
    <line x1="414" y1="54" x2="540" y2="54" stroke="#8A919C" stroke-width="2"/>
    <polygon points="540,49 552,54 540,59" fill="#8A919C"/>
    <text x="477" y="30" text-anchor="middle" fill="#8A919C" font-size="11">lock 1:1</text>
    <rect x="552" y="34" width="72" height="40" rx="6" fill="#0C0F14" stroke="#1C222C" stroke-width="2"/>
    <text x="588" y="59" text-anchor="middle" fill="#E8EBF0" font-weight="600" font-size="14">M1</text>
    <text x="222" y="98" text-anchor="middle" fill="#5B626E" font-size="11">no reserve · no redemption · nothing flows back along this arrow</text>
  </g>
</svg>

```text
BTC --one-way, SPV-proven destruction--> M0 --lock 1:1--> M1
                                          (no reserve · no redemption)
```

Because the arrow only points one way, three things follow in plain words:

- **There is no reserve.** The destroyed BTC is gone. Nobody holds it, so nobody can lose it,
  freeze it or lend it out.
- **There is no redemption.** M1 cannot be handed back to the protocol in exchange for BTC.
  There is no counter to walk up to.
- **M1 has no external peg.** The 1:1 rule between M0 and M1 is an internal accounting rule
  ([invariants](../reference/invariants.md)); it says nothing about what M1 is worth in BTC on
  any given day. M1 is a settlement unit that market builders and providers use as a pivot —
  not a claim on Bitcoin.

That is why this site never describes M1 as *backed*. Backing implies a reserve and a
redemption promise; there is neither. M1 *originates* from Bitcoin — a different thing.

## How native BTC comes back: the market

If the protocol cannot give BTC back, what makes native BTC available again is the market.
Someone who holds M1 and wants BTC finds a counterparty who holds BTC and wants M1 — a
Liquidity Provider, another user, anyone with inventory — and the two sides settle through
paired hashlocked contracts: an M1 HTLC on BATHRON and a Bitcoin HTLC on Bitcoin, sharing one
preimage. The protocol guarantees the M1 leg; the Bitcoin leg is an ordinary Bitcoin contract;
the pairing is what makes the exchange safe for both sides.

This is the [native BTC ⇄ M1 pair](../markets/native-btc-pair.md) — the first and most
important market on BATHRON, and one the protocol does not run. It exists because providers
choose to quote it.

**See also:** [From destroyed BTC to M1](from-btc-to-m1.md) · [Status & claims](../consensus/status-and-claims.md)
