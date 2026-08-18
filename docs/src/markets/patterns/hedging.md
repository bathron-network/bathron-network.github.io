# Hedging on Bitcoin facts

A miner's revenue is a bet on Bitcoin's difficulty. Hedging that bet normally requires a broker
and a price feed — a counterparty and someone to *report* the number. On BATHRON the
settlement condition can be Bitcoin's own difficulty, read by consensus from the header chain
it already carries. A market for difficulty hedges can therefore exist without a designated
reporter, and anyone can build one.

```text
  miner ─────┐                       ┌───── counterparty
             ▼                       ▼
        both lock margin in a covenant
                       │
                       ▼
   at expiry: consensus reads Bitcoin difficulty
        from the in-consensus header chain
                       │
          difficulty rose        difficulty fell
                │                       │
                ▼                       ▼
         pays the miner        pays the counterparty
```

## Why this is different

Every difficulty derivative elsewhere trusts someone to report difficulty. On BATHRON the
header chain — with its difficulty adjustments — **is consensus state**: the covenant reads the
fact itself. There is no reporter to bribe and no publisher to go offline. Scripts can inspect
difficulty, timestamps and accumulated chainwork the same way (see
[Bitcoin facts inside consensus](../../bitcoin/facts-in-consensus.md)).

## The honest caveat

Difficulty can be verified without an external reporter because Bitcoin publishes it. This
still relies on BATHRON's Bitcoin-header validation, its Operator-finality assumptions and the
software used by the parties. A full *hashprice* hedge also involves the BTC price — which is
not an on-chain fact and needs a signed input (`CSFS`), with the additional trust in that
signer which it implies.

**Primitives:** in-consensus Bitcoin headers · difficulty introspection · covenants · `CSFS`
(price leg only)

**See also:** [Fixed-term value positions](fixed-term-value.md)
