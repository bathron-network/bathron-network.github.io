# Examples

## Tested components of a conditional settlement

The testnet has exercised the main components needed by the product hypothesis:

**Bitcoin fact verification.** A signet payment and Merkle branch were checked against the
Bitcoin header chain carried in BATHRON consensus. `TX_CONFIRMED` then released a CTV-constrained
internal covenant.

**Confidential internal hop.** Provider-controlled test inventory moved through Sapling while the
M0/M1 conservation invariants remained valid. This demonstrates confidential settlement state;
it is not a retail wallet flow.

**Paired HTLCs.** An M1 HTLC on BATHRON and a P2WSH HTLC on signet used the same hashlock. The
test claimed both legs and verified the same preimage on each chain.

```text
Bitcoin proof -> internal covenant -> confidential provider state
                                          |
recipient BTC <- paired HTLC test <- CP/LP prototype
```

These observations do not yet prove a generally atomic client service. Before making that claim,
an application must specify every intermediate state, Bitcoin reorganisation rule, timelock order
and refund branch, then undergo external review.

## Where the code lives

The node, tools and application code are published across the
[BATHRON GitHub organization](https://github.com/bathron-network). Runnable SDK patterns ship
with the public testnet.
