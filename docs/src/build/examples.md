# Examples

## Tested components of a conditional settlement

The testnet has exercised the main components needed by the product hypothesis:

**Bitcoin fact verification.** A payment on the Bitcoin test network and its Merkle branch were
checked against the Bitcoin header chain carried in BATHRON consensus (the chain read by
consensus today is Bitcoin testnet4). `TX_CONFIRMED` then released a CTV-constrained internal
covenant.

**Confidential internal hop.** Provider-controlled test inventory moved through Sapling while the
M0/M1 conservation invariants remained valid. This demonstrates confidential settlement state;
it is not a retail wallet flow.

**Paired HTLCs.** An M1 HTLC on BATHRON and a P2WSH HTLC on the Bitcoin test network used the
same hashlock. The test claimed both legs and verified the same preimage on each chain. This is
the mechanism behind the [native BTC ⇄ M1 pair](../markets/native-btc-pair.md).

```text
Bitcoin proof -> internal covenant -> confidential provider state
                                          |
recipient BTC <- paired HTLC test <- CP/LP prototype
```

These observations do not yet prove a generally atomic client service; see
[Status & claims](../consensus/status-and-claims.md).

## Where the code lives

The node, tools and application code are published across the
[BATHRON GitHub organization](https://github.com/bathron-network). Runnable SDK patterns ship
with the public testnet. The CP/LP prototypes (`pna-lp`, `pna-swap`) are described in
[Create your first market](../operate/create-your-first-market.md).

**See also:** [Settlement patterns](../markets/patterns.md) ·
[Build your first application](../operate/first-application.md)
