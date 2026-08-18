# Native BTC ⇄ M1: the atomic pair

Every market on BATHRON is a pair against M1, and the pair that matters first is Bitcoin
itself: without a way for native BTC to enter and leave M1, no other market can be priced in
BTC terms. The burn route creates M1 once and irreversibly (see
[From destroyed BTC to M1](../bitcoin/from-btc-to-m1.md)); the atomic pair is how BTC and M1
change hands afterwards — reversibly, repeatedly, and without anyone holding either side.

## The mechanism: two locks, one secret

BATHRON can verify Bitcoin facts, but it cannot move native BTC or trigger a Bitcoin
transaction. So the BTC leg is an ordinary Bitcoin transaction, and the two legs are tied
together by a shared secret rather than by a custodian.

```text
  Bitcoin                                   BATHRON
  ────────                                  ────────
  P2WSH HTLC: pay to hash H, or             M1 HTLC: pay to hash H, or
  refund after CLTV timeout T_btc           refund after timeout T_m1
        │                                          │
        └───────────── same hash H ────────────────┘
                              │
        claiming one leg reveals the preimage of H —
        the other leg becomes claimable with it
                              │
              both settle, or both refund on timeout
```

1. The two parties agree on a price off-chain (a quote from a Liquidity Provider, or a direct
   negotiation — the protocol does not care).
2. One side locks BTC in a Bitcoin P2WSH script: spendable with the preimage of `H`, or
   refundable to the sender after a `CLTV` timeout.
3. The other side locks M1 on BATHRON under a hashlock keyed to the **same** `H`, with a
   shorter timeout.
4. The party holding the secret claims the leg it wants; that claim publishes the preimage on
   chain, and the counterparty uses it to claim the other leg.
5. If either side walks away, both timeouts fire and each party is refunded.

The timeout on the leg locked second is shorter than the timeout on the leg locked first, so
that a party who learns the preimage cannot claim one leg while the other has already refunded.

The same construction works with a proof instead of a preimage: a BATHRON covenant can release
M1 when `TX_CONFIRMED` proves that a given Bitcoin payment is buried under the in-consensus
header chain (see [Bitcoin facts inside consensus](../bitcoin/facts-in-consensus.md)).

## What this gives a market

- Native BTC enters M1 and leaves M1 without a custodian, a bridge or a wrapped asset.
- Bitcoin sees two unremarkable transactions; the size and counterparties of the trade can
  stay shielded on the BATHRON side (see [Confidential settlement](confidential-settlement.md)).
- Any chain with hashlocks and timelocks can be paired the same way — a capability, not a
  shipped product (see [Pairing any asset against M1](pairing-any-asset.md)).

## Known limit: the initiator's free option

Between the two locks the initiator can wait and decide whether to complete or let the trade
time out, depending on how the price moved; this "free option" is priced by the counterparty
(premium, collateral, short timeouts), not eliminated by the protocol.

## What was demonstrated

On testnet, paired-HTLC components have been exercised end to end: an M1 HTLC on BATHRON and a
Bitcoin P2WSH HTLC keyed to the same preimage, both legs claimed and the same preimage verified
on each chain. A general atomic client service — every intermediate state, reorganisation rule
and refund branch specified and reviewed — is not claimed; see
[Status & claims](../consensus/status-and-claims.md).

**Primitives:** hashlocks (HTLC) · `CLTV` / `CSV` · `TX_CONFIRMED` · shielded transfers

**See also:** [Delivery-versus-payment and OTC](patterns/dvp-otc.md) ·
[Create your first market](../operate/create-your-first-market.md)
